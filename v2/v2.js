/* Bellandur Ganesha Utsava v2.

   Almost nothing. The sheet-stacking scroll engine that seeded this page was
   cut: it measurably covered content before it could be read, and it carried
   a sticky-position layout pass, a scrim ramp, ghost parallax and an anchor
   correction that only existed to work around itself. Sections now follow one
   another in normal flow, so smooth anchor scrolling is the browser's job and
   scroll position needs no JavaScript at all.

   What is left is the one behaviour a stylesheet cannot express: on phones the
   detail rows collapse, and tapping a title expands it. */
(function () {
  'use strict';

  var mqPhone = window.matchMedia('(max-width: 640px)');
  var rows = Array.prototype.slice.call(document.querySelectorAll('.row'));
  if (!rows.length) return;

  function toggleRow(row) {
    var open = row.classList.toggle('is-open');
    row.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  /* The rows are only interactive at phone widths, so the button semantics
     have to come and go with the media query rather than sit in the markup. */
  function syncRowRoles() {
    rows.forEach(function (row) {
      if (mqPhone.matches) {
        row.setAttribute('role', 'button');
        row.setAttribute('tabindex', '0');
        row.setAttribute('aria-expanded', row.classList.contains('is-open') ? 'true' : 'false');
      } else {
        row.removeAttribute('role');
        row.removeAttribute('tabindex');
        row.removeAttribute('aria-expanded');
      }
    });
  }

  rows.forEach(function (row) {
    row.addEventListener('click', function (e) {
      if (!mqPhone.matches) return;
      if (e.target.closest('a')) return;
      toggleRow(row);
    });
    row.addEventListener('keydown', function (e) {
      if (!mqPhone.matches) return;
      if (e.key !== 'Enter' && e.key !== ' ') return;
      e.preventDefault();
      toggleRow(row);
    });
  });

  syncRowRoles();
  mqPhone.addEventListener('change', syncRowRoles);
})();
