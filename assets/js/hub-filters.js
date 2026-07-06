(function () {
  function initFilters(root) {
    var fields = root.querySelectorAll(".el-filters__field");
    if (!fields.length) return;

    fields.forEach(function (field) {
      field.addEventListener("toggle", function () {
        if (!field.open) return;
        fields.forEach(function (other) {
          if (other !== field) other.open = false;
        });
      });
    });

    document.addEventListener("click", function (event) {
      if (root.contains(event.target)) return;
      fields.forEach(function (field) {
        field.open = false;
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key !== "Escape") return;
      fields.forEach(function (field) {
        field.open = false;
      });
    });
  }

  document.querySelectorAll("[data-el-filters]").forEach(initFilters);
})();
