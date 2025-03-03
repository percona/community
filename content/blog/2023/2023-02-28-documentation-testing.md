---
title: "How to test code blocks in documentation"
date: "2023-02-28T00:00:00+00:00"
tags: ["Documentation","Testing", "Pandoc"]
categories: ["Community", "PMM"]
authors:
  - denys_kondratenko
images:
  - blog/2023/02/doc-testing.jpg
slug: doc-testing
---

As any developer, I don't like to write documentation. But if I am writing it, I would like to test that what I wrote works.
I often found myself copy-pasting something from documentation and trying to run it in the terminal (commands, files, etc.), and it didn't work.

There are usually some environment, typos, or even wrong commands in the doc (that people copy-pasted from the wrong place).

I know that issue, and after writing the documentation, I usually try to clean up everything in my environment and test the doc. I am reading it and executing commands as they wrote. Sometimes I find something needs to be fixed. So I needed to find a way to test it quickly.

For example, recent [Podman](https://github.com/percona/pmm-doc/blob/main/docs/setting-up/server/podman.md) doc has both code and files:

```
    You can override the environment variables by defining them in the file  `~/.config/pmm-server/env`. For example, to override the path to a custom registry `~/.config/pmm-server/env`:

    ```sh
    mkdir -p ~/.config/pmm-server/
    cat << "EOF" > ~/.config/pmm-server/env
    PMM_TAG=2.35.0
    PMM_IMAGE=docker.io/percona/pmm-server
    PMM_PUBLIC_PORT=8443
    EOF
    ```

    !!! caution alert alert-warning "Important"
        Ensure that you modify PMM_TAG in `~/.config/pmm-server/env` and update it regularly as Percona cannot update it. It needs to be done by you.

1. Enable and Start.

    ```sh
    systemctl --user enable --now pmm-server
    ```

```

Documentation ages and there could be new images that wouldn't work with this documentation anymore.
Another issue is making changes to the existing documentation - how to know that there are no regressions with something new added or with some fixes?

Usually, to mitigate those issues, developers and/or tech writers are \[re\]checking everything manually.

There are many different automatic approaches to mitigate that issue. The ultimate solution for this is probably [GNU Emacs Org Mode](https://orgmode.org/). I dream that one day I will learn Emacs and Org Mode.

But I need a solution now, and the team process is to have documentation in a Markdown format and track everything in GitHub - [PMM Documentation](https://github.com/percona/pmm-doc). [GitHub](#github) supports quite good code formating, and it is easy to develop and review Markdown there.

There are probably [frameworks](#frameworks) that could help with that, but I needed something quick and didn't want to introduce yet another testing framework to the batch.

So I was looking for something that would allow me to quickly cut code snippets from the documentation and run them in a GitHub action. While searching, I found this doc blog: [Test codeblocks in markdown documents](https://tomlankhorst.nl/testing-code-in-markdown-doc-md-github). Which was exactly what I needed :)

The only problem I found out quickly is that I need something else. Pandoc builds AST tree just fine:

```json
            {
              "t": "CodeBlock",
              "c": [
                [
                  "",
                  [
                    "sh"
                  ],
                  []
                ],
                "mkdir -p ~/.config/pmm-server/\ncat << \"EOF\" > ~/.config/pmm-server/env\nPMM_TAG=2.35.0\nPMM_IMAGE=docker.io/percona/pmm-server\nPMM_PUBLIC_PORT=8443\nEOF"
              ]
            },
...
            {
              "t": "CodeBlock",
              "c": [
                [
                  "",
                  [
                    "sh"
                  ],
                  []
                ],
                "systemctl --user enable --now pmm-server"
              ]
            }
...
        [
          {
            "t": "CodeBlock",
            "c": [
              [
                "",
                [
                  "sh"
                ],
                []
              ],
              "#first pull can take time\nsleep 80\ntimeout 60 podman wait --condition=running pmm-server"
            ]
          }
        ]
```

As you see, the 3rd `CodeBlock` is not on the same level. So when using `jq` approach (from the blog post):

```
pandoc -i podman.md -t json | jq -r -c '.blocks[] | select(.t | contains("CodeBlock"))? | .c'

[["",[],[]],"```sh\npodman exec -it pmm-server \\\ncurl -ku admin:admin https://localhost/v1/version\n```"]p'
```

It returns only the block from that level that `jq` program specifies. My first reaction was to try to advance that filter, but there were so many levels of code block that could be found, and there was so much I needed to learn and do to create the number of filters that I abandoned the idea.

Still, [Pandoc](#pandoc) is a very powerful tool, so I started digging to find out if any embedded filters could help me filter only `CodeBlocks`. And apparently, there are [Pandoc Lua Filters](https://pandoc.org/lua-filters.html). After some experiments, I came up with the following:
```lua
traverse = 'topdown'
function CodeBlock(block)
    if block.classes[1] == "sh" then
        print("#-----CodeBlock-----")
        io.stdout:write(block.text,"\n\n")
    end
    return nil
end
```

This gives me a sequence of blocks that are marked as `sh`:

```sh
 pandoc -i podman.md --lua-filter ../../../_resources/bin/CodeBlock.lua -t html -o /dev/null

...
#-----CodeBlock-----
mkdir -p ~/.config/pmm-server/
cat << "EOF" > ~/.config/pmm-server/env
PMM_TAG=2.31.0
PMM_IMAGE=docker.io/percona/pmm-server
PMM_PUBLIC_PORT=8443
EOF

#-----CodeBlock-----
systemctl --user enable --now pmm-server
```

So that is easy to wrap up in a shell script and execute - locally or in a [GitHub Action](https://github.com/percona/pmm-doc/blob/main/.github/workflows/podman-tests.yml#L35):

```
      - name: Copy test template
        run: cp _resources/bin/doc_test_template.sh ./docs_test_podman.sh

      - name: Get CodeBlocks and push them to test template
        run: pandoc -i docs/setting-up/server/podman.md --lua-filter _resources/bin/CodeBlock.lua -t html -o /dev/null >> docs_test_podman.sh

      - name: Run podman tests
        run: ./docs_test_podman.sh
```

Sometimes, you will find yourself in a situation where you need to execute something (env, infra, cleanup) that should not be shown in the documentation. For example, wait for the previous action before the next one:

```
<div hidden>
```
```sh
sleep 30
timeout 60 podman wait --condition=running pmm-server
```
```
</div>
```

I use `html` to hide `CodeBlocks` from the rendered document.

You could solve documentation testing at least for some or most of the cases with these simple conventions:
- `sh` language identifier for the fenced code blocks for examples
- `<div hidden>` for code blocks that should not be in the rendered documentation
- [Bash Heredoc](https://linuxize.com/post/bash-heredoc/) for files

This approach is easy to use locally to test documentation you just wrote and integrate into the CI pipeline.

## Links

Here are some links. If you have some more suggestions - please open an issue or PR: https://github.com/percona/community/ .

### Editors

- https://orgmode.org/
- http://howardism.org/Technical/Emacs/literate-devops.html

### GitHub

- Library is used on GitHub.com to detect blob languages: https://github.com/github/linguist/blob/master/lib/linguist/languages.yml
- https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-and-highlighting-code-blocks

### Frameworks

- https://github.com/Widdershin/markdown-doctest
- https://github.com/nschloe/pytest-codeblocks

### Pandoc

- https://tomlankhorst.nl/testing-code-in-markdown-doc-md-github
- https://pandoc.org/MANUAL.html
- https://pandoc.org/filters.html
- https://pandoc.org/lua-filters.html
