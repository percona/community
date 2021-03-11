# Percona Blog Website Project

## How to Run on MacOs

You need to install Git and Hugo:

1. Install Homebrew if it is not installed.

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. Install Git.

```
brew install git
```
3. Install Hugo.

```
brew install hugo
```
4. Clone the repository.

```
git clone https://github.com/percona/community.git
```
5. Go to the Community folder.

```
cd community
```
5. Run Hugo

```
hugo server -D
```
6. Open the URL that Hugo indicates you in Terminal, for example http://localhost:1313/. You will see the project.

7. Use CTRL + C to stop the server. If you need to kill the old ports, run:

```
killall -9 hugo
```
