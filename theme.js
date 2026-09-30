// Theme controller. Load synchronously in <head> so the saved theme is
// applied before first paint (no light/dark flash).
(function () {
  var KEY = 'theme';
  var root = document.documentElement;

  function read() {
    try { return localStorage.getItem(KEY) || 'system'; } catch (e) { return 'system'; }
  }

  function apply(choice) {
    if (choice === 'light' || choice === 'dark') {
      root.setAttribute('data-theme', choice);
    } else {
      root.removeAttribute('data-theme');
    }
  }

  function save(choice) {
    try { localStorage.setItem(KEY, choice); } catch (e) { /* storage unavailable */ }
  }

  apply(read());

  // Wire any .theme-toggle radio groups once the DOM is ready.
  document.addEventListener('DOMContentLoaded', function () {
    var current = read();
    document.querySelectorAll('.theme-toggle input[type="radio"]').forEach(function (input) {
      input.checked = input.value === current;
      input.addEventListener('change', function () {
        apply(input.value);
        save(input.value);
      });
    });
  });
})();
