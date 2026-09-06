(function () {
  var THEME_KEY = "bgu-theme";
  var LANG_KEY = "bgu-lang";
  var root = document.documentElement;
  var themeMeta = document.querySelector('meta[name="theme-color"]');

  var strings = {
    en: {
      "nav.resources": "Resources",
      "nav.home": "Back to home",
      "theme.toLight": "Light",
      "theme.toDark": "Dark",
      "home.sub": "ಬೆಳಂದೂರು ಗಣೇಶ ಉತ್ಸವ",
      "home.title": "Bellandur Ganesha Utsava",
      "home.lead":
        "A prominent 5-day community festival in Bellandur, Bengaluru, known for one of the tallest and richest Ganesha idols in the area.",
      "home.ctaDates": "See dates",
      "home.ctaDonate": "Donate",
      "home.swipe": "Swipe up",
      "about.eyebrow": "About",
      "about.title": "10th year of devotion",
      "about.body":
        "Organised by Sri Vinayaka Seva Mandali and Classic Boys, Bellandur Ganesha Utsava draws massive local crowds for daily rituals and the grand procession. This is the 10th year of the festival in Bellandur.",
      "about.orgTitle": "Organised by",
      "about.orgBody": "Sri Vinayaka Seva Mandali & Classic Boys",
      "about.venueTitle": "Location",
      "about.venueBody":
        "Near Shri Venkateshwara Swamy Temple, 12th B Cross Rd, Bellandur, Bengaluru, Karnataka 560103",
      "dates.eyebrow": "Dates",
      "dates.title": "5-day festival",
      "dates.boxTitle": "Exact dates TBA",
      "dates.boxBody":
        "Five days starting from Ganesh Chaturthi. Add the official calendar dates here when published.",
      "dates.d1slot": "Day 1",
      "dates.d1title": "Ganesh Chaturthi opening & first rituals",
      "dates.d2slot": "Days 2 to 4",
      "dates.d2title": "Daily poojas and community rituals",
      "dates.d3slot": "Day 5",
      "dates.d3title": "Grand procession and visarjan",
      "prog.eyebrow": "Programmes",
      "prog.title": "What to expect",
      "prog.body":
        "Daily rituals around a landmark Ganesha idol, community gatherings, and a grand visarjan procession. Detailed programme slots below are placeholders.",
      "prog.s1slot": "Idol",
      "prog.s1title": "One of the tallest and richest Ganesha idols in the area",
      "prog.s2slot": "Daily",
      "prog.s2title": "Poojas, aarti, and community rituals",
      "prog.s3slot": "Crowds",
      "prog.s3title": "Massive local turnout across five days",
      "prog.s4slot": "Finale",
      "prog.s4title": "Grand procession and visarjan",
      "photos.eyebrow": "Gallery",
      "photos.title": "Photos & videos",
      "photos.body":
        "Follow @bellanduru_ganesha_utsava on Instagram, browse the photo album, or watch Facebook videos.",
      "photos.label": "Open photo album",
      "photos.cta": "View album",
      "photos.instagram": "Instagram",
      "photos.facebook": "Facebook videos",
      "donate.eyebrow": "Support",
      "donate.title": "Donate",
      "donate.body":
        "Support Sri Vinayaka Seva Mandali and Classic Boys with pooja arrangements, the idol, and community seva. Scan the QR once it is published.",
      "donate.qr": "QR code\nplaceholder",
      "donate.boxTitle": "UPI / bank details",
      "donate.boxBody": "Placeholder for UPI ID, account name, and receipt contact.",
      "res.eyebrow": "Brand",
      "res.title": "Logos & assets",
      "res.body":
        "Download English and Kannada logo files for posters, invites, and social posts.",
      "res.cta": "Open resources",
      "res.top": "Back to top",
      "res.pageTitle": "Resources",
      "res.pageLead": "Official logo files for print and digital use. Prefer SVG for scale.",
      "res.enHeading": "English logos",
      "res.knHeading": "Kannada logos",
      "res.cherryTitle": "Cherry & gold",
      "res.cherryEn": "Primary mark for light grounds. Cream disc, cherry ink.",
      "res.cherryKn": "Primary Kannada colour mark.",
      "res.revTitle": "Reversed",
      "res.revBody": "Gold on cherry, for dark or photographic grounds.",
      "res.origTitle": "Original colourway",
      "res.origBody": "Orange and gold trace, crown dots removed.",
      "res.sheetHeading": "Contact sheet",
      "res.sheetTitle": "All six variants",
      "res.sheetBody": "One sheet with every colourway, for quick reference.",
      "res.note":
        "Use these files for festival communication only. Keep clear space around the mark and do not recolour the emblem outside the provided variants.",
      "dot.Home": "Home",
      "dot.About": "About",
      "dot.Dates": "Dates",
      "dot.Programmes": "Programmes",
      "dot.Photos": "Photos",
      "dot.Donate": "Donate",
      "dot.Resources": "Resources",
      "doc.title": "Bellandur Ganesha Utsava",
      "doc.resourcesTitle": "Resources | Bellandur Ganesha Utsava"
    },
    kn: {
      "nav.resources": "ಸಂಪನ್ಮೂಲಗಳು",
      "nav.home": "ಮುಖಪುಟಕ್ಕೆ",
      "theme.toLight": "ಬೆಳಕು",
      "theme.toDark": "ಕತ್ತಲೆ",
      "home.sub": "Bellandur Ganesha Utsava",
      "home.title": "ಬೆಳಂದೂರು ಗಣೇಶ ಉತ್ಸವ",
      "home.lead":
        "ಬೆಳಂದೂರು, ಬೆಂಗಳೂರಿನ ಪ್ರಮುಖ ೫ ದಿನಗಳ ಸಮುದಾಯ ಉತ್ಸವ. ಈ ಪ್ರದೇಶದ ಅತಿ ಎತ್ತರದ ಮತ್ತು ಸಂಪನ್ನ ಗಣೇಶ ಮೂರ್ತಿಗಳಲ್ಲಿ ಒಂದಕ್ಕೆ ಹೆಸರುವಾಸಿ.",
      "home.ctaDates": "ದಿನಾಂಕಗಳು",
      "home.ctaDonate": "ದಾನ",
      "home.swipe": "ಮೇಲಕ್ಕೆ ಸ್ವೈಪ್",
      "about.eyebrow": "ಪರಿಚಯ",
      "about.title": "೧೦ನೇ ವರ್ಷದ ಭಕ್ತಿ",
      "about.body":
        "ಶ್ರೀ ವಿನಾಯಕ ಸೇವಾ ಮಂಡಲಿ ಮತ್ತು ಕ್ಲಾಸಿಕ್ ಬಾಯ್ಸ್ ಆಯೋಜಿಸುವ ಬೆಳಂದೂರು ಗಣೇಶ ಉತ್ಸವವು ದೈನಂದಿನ ಆಚರಣೆಗಳು ಮತ್ತು ವಿಶಾಲ ಮೆರವಣಿಗೆಗಾಗಿ ದೊಡ್ಡ ಸ್ಥಳೀಯ ಜನಸಂದಣಿಯನ್ನು ಸೆಳೆಯುತ್ತದೆ. ಇದು ಬೆಳಂದೂರಿನಲ್ಲಿ ಉತ್ಸವದ ೧೦ನೇ ವರ್ಷ.",
      "about.orgTitle": "ಆಯೋಜಕರು",
      "about.orgBody": "ಶ್ರೀ ವಿನಾಯಕ ಸೇವಾ ಮಂಡಲಿ ಮತ್ತು ಕ್ಲಾಸಿಕ್ ಬಾಯ್ಸ್",
      "about.venueTitle": "ಸ್ಥಳ",
      "about.venueBody":
        "ಶ್ರೀ ವೆಂಕಟೇಶ್ವರ ಸ್ವಾಮಿ ದೇವಸ್ಥಾನದ ಹತ್ತಿರ, ೧೨ನೇ ಬಿ ಕ್ರಾಸ್ ರಸ್ತೆ, ಬೆಳಂದೂರು, ಬೆಂಗಳೂರು, ಕರ್ನಾಟಕ ೫೬೦೧೦೩",
      "dates.eyebrow": "ದಿನಾಂಕಗಳು",
      "dates.title": "೫ ದಿನಗಳ ಉತ್ಸವ",
      "dates.boxTitle": "ನಿಖರ ದಿನಾಂಕಗಳು ಶೀಘ್ರದಲ್ಲೇ",
      "dates.boxBody":
        "ಗಣೇಶ ಚತುರ್ಥಿಯಿಂದ ಆರಂಭವಾಗುವ ಐದು ದಿನಗಳು. ಅಧಿಕೃತ ಕ್ಯಾಲೆಂಡರ್ ದಿನಾಂಕಗಳನ್ನು ಪ್ರಕಟವಾದಾಗ ಸೇರಿಸಿ.",
      "dates.d1slot": "ದಿನ ೧",
      "dates.d1title": "ಗಣೇಶ ಚತುರ್ಥಿ ಉದ್ಘಾಟನೆ ಮತ್ತು ಮೊದಲ ಆಚರಣೆಗಳು",
      "dates.d2slot": "ದಿನ ೨ ರಿಂದ ೪",
      "dates.d2title": "ದೈನಂದಿನ ಪೂಜೆಗಳು ಮತ್ತು ಸಮುದಾಯ ಆಚರಣೆಗಳು",
      "dates.d3slot": "ದಿನ ೫",
      "dates.d3title": "ವಿಶಾಲ ಮೆರವಣಿಗೆ ಮತ್ತು ವಿಸರ್ಜನೆ",
      "prog.eyebrow": "ಕಾರ್ಯಕ್ರಮಗಳು",
      "prog.title": "ಏನನ್ನು ನಿರೀಕ್ಷಿಸಬಹುದು",
      "prog.body":
        "ವಿಶೇಷ ಗಣೇಶ ಮೂರ್ತಿಯ ಸುತ್ತ ದೈನಂದಿನ ಆಚರಣೆಗಳು, ಸಮುದಾಯ ಸೇರುವಿಕೆ ಮತ್ತು ವಿಸರ್ಜನೆ ಮೆರವಣಿಗೆ. ಕೆಳಗಿನ ವಿವರಗಳು ತಾತ್ಕಾಲಿಕ.",
      "prog.s1slot": "ಮೂರ್ತಿ",
      "prog.s1title": "ಈ ಪ್ರದೇಶದ ಅತಿ ಎತ್ತರದ ಮತ್ತು ಸಂಪನ್ನ ಗಣೇಶ ಮೂರ್ತಿಗಳಲ್ಲಿ ಒಂದು",
      "prog.s2slot": "ದೈನಂದಿನ",
      "prog.s2title": "ಪೂಜೆ, ಆರತಿ ಮತ್ತು ಸಮುದಾಯ ಆಚರಣೆಗಳು",
      "prog.s3slot": "ಜನಸಂದಣಿ",
      "prog.s3title": "ಐದು ದಿನಗಳಲ್ಲಿ ದೊಡ್ಡ ಸ್ಥಳೀಯ ಭಾಗವಹಿಸುವಿಕೆ",
      "prog.s4slot": "ಅಂತ್ಯ",
      "prog.s4title": "ವಿಶಾಲ ಮೆರವಣಿಗೆ ಮತ್ತು ವಿಸರ್ಜನೆ",
      "photos.eyebrow": "ಚಿತ್ರಗಳು",
      "photos.title": "ಫೋಟೋ ಮತ್ತು ವೀಡಿಯೊಗಳು",
      "photos.body":
        "Instagram ನಲ್ಲಿ @bellanduru_ganesha_utsava ಅನುಸರಿಸಿ, ಫೋಟೋ ಆಲ್ಬಮ್ ನೋಡಿ, ಅಥವಾ Facebook ವೀಡಿಯೊಗಳನ್ನು ನೋಡಿ.",
      "photos.label": "ಫೋಟೋ ಆಲ್ಬಮ್ ತೆರೆಯಿರಿ",
      "photos.cta": "ಆಲ್ಬಮ್ ನೋಡಿ",
      "photos.instagram": "Instagram",
      "photos.facebook": "Facebook ವೀಡಿಯೊಗಳು",
      "donate.eyebrow": "ಬೆಂಬಲ",
      "donate.title": "ದಾನ",
      "donate.body":
        "ಶ್ರೀ ವಿನಾಯಕ ಸೇವಾ ಮಂಡಲಿ ಮತ್ತು ಕ್ಲಾಸಿಕ್ ಬಾಯ್ಸ್ ಅವರ ಪೂಜಾ ವ್ಯವಸ್ಥೆ, ಮೂರ್ತಿ ಮತ್ತು ಸಮುದಾಯ ಸೇವೆಗೆ ಬೆಂಬಲಿಸಿ. QR ಪ್ರಕಟವಾದ ನಂತರ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ.",
      "donate.qr": "QR ಕೋಡ್\nತಾತ್ಕಾಲಿಕ",
      "donate.boxTitle": "UPI / ಬ್ಯಾಂಕ್ ವಿವರಗಳು",
      "donate.boxBody": "UPI ID, ಖಾತೆ ಹೆಸರು ಮತ್ತು ರಸೀದಿ ಸಂಪರ್ಕಕ್ಕೆ ತಾತ್ಕಾಲಿಕ ಸ್ಥಳ.",
      "res.eyebrow": "ಬ್ರಾಂಡ್",
      "res.title": "ಲೋಗೋ ಮತ್ತು ಸಂಪತ್ತು",
      "res.body":
        "ಪೋಸ್ಟರ್, ಆಮಂತ್ರಣ ಮತ್ತು ಸಾಮಾಜಿಕ ಪೋಸ್ಟ್‌ಗಳಿಗೆ ಇಂಗ್ಲಿಷ್ ಮತ್ತು ಕನ್ನಡ ಲೋಗೋಗಳನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ.",
      "res.cta": "ಸಂಪನ್ಮೂಲಗಳು",
      "res.top": "ಮೇಲಕ್ಕೆ",
      "res.pageTitle": "ಸಂಪನ್ಮೂಲಗಳು",
      "res.pageLead": "ಮುದ್ರಣ ಮತ್ತು ಡಿಜಿಟಲ್ ಬಳಕೆಗೆ ಅಧಿಕೃತ ಲೋಗೋಗಳು. ಸ್ಕೇಲ್‌ಗೆ SVG ಉತ್ತಮ.",
      "res.enHeading": "ಇಂಗ್ಲಿಷ್ ಲೋಗೋಗಳು",
      "res.knHeading": "ಕನ್ನಡ ಲೋಗೋಗಳು",
      "res.cherryTitle": "ಚೆರ್ರಿ ಮತ್ತು ಚಿನ್ನ",
      "res.cherryEn": "ತಿಳಿ ಹಿನ್ನೆಲೆಗೆ ಪ್ರಾಥಮಿಕ ಗುರುತು. ಕೆನೆ ಬಣ್ಣದ ಬಿಂಬ, ಚೆರ್ರಿ ಶಾಯಿ.",
      "res.cherryKn": "ಪ್ರಾಥಮಿಕ ಕನ್ನಡ ಬಣ್ಣದ ಗುರುತು.",
      "res.revTitle": "ವಿಲೋಮ",
      "res.revBody": "ಚೆರ್ರಿ ಮೇಲೆ ಚಿನ್ನ, ಕತ್ತಲೆ ಅಥವಾ ಚಿತ್ರ ಹಿನ್ನೆಲೆಗೆ.",
      "res.origTitle": "ಮೂಲ ಬಣ್ಣ",
      "res.origBody": "ಕಿತ್ತಳೆ ಮತ್ತು ಚಿನ್ನ, ಕಿರೀಟದ ಚುಕ್ಕೆಗಳು ತೆಗೆದಿವೆ.",
      "res.sheetHeading": "ಸಂಪರ್ಕ ಹಾಳೆ",
      "res.sheetTitle": "ಎಲ್ಲಾ ಆರು ರೂಪಗಳು",
      "res.sheetBody": "ಎಲ್ಲಾ ಬಣ್ಣದ ರೂಪಗಳು ಒಂದೇ ಹಾಳೆಯಲ್ಲಿ, ತ್ವರಿತ ಉಲ್ಲೇಖಕ್ಕೆ.",
      "res.note":
        "ಈ ಕಡತಗಳನ್ನು ಉತ್ಸವ ಸಂವಹನಕ್ಕೆ ಮಾತ್ರ ಬಳಸಿ. ಗುರುತಿನ ಸುತ್ತ ಸ್ಪಷ್ಟ ಸ್ಥಳಾವಕಾಶ ಇರಿಸಿ ಮತ್ತು ನೀಡಲಾದ ರೂಪಗಳ ಹೊರಗೆ ಬಣ್ಣ ಬದಲಿಸಬೇಡಿ.",
      "dot.Home": "ಮುಖ್ಯ",
      "dot.About": "ಪರಿಚಯ",
      "dot.Dates": "ದಿನಾಂಕ",
      "dot.Programmes": "ಕಾರ್ಯಕ್ರಮ",
      "dot.Photos": "ಚಿತ್ರಗಳು",
      "dot.Donate": "ದಾನ",
      "dot.Resources": "ಸಂಪನ್ಮೂಲ",
      "doc.title": "ಬೆಳಂದೂರು ಗಣೇಶ ಉತ್ಸವ",
      "doc.resourcesTitle": "ಸಂಪನ್ಮೂಲಗಳು | ಬೆಳಂದೂರು ಗಣೇಶ ಉತ್ಸವ"
    }
  };

  function readStored(key, fallback) {
    try {
      return localStorage.getItem(key) || fallback;
    } catch (e) {
      return fallback;
    }
  }

  function writeStored(key, value) {
    try {
      localStorage.setItem(key, value);
    } catch (e) {
      /* ignore */
    }
  }

  function currentTheme() {
    return root.getAttribute("data-theme") === "light" ? "light" : "dark";
  }

  function currentLang() {
    return root.getAttribute("data-lang") === "kn" ? "kn" : "en";
  }

  function assetBase() {
    return document.body.getAttribute("data-asset-base") || "";
  }

  function applyTheme(theme) {
    var next = theme === "light" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    writeStored(THEME_KEY, next);
    if (themeMeta) {
      themeMeta.setAttribute("content", next === "light" ? "#FFF8EC" : "#6B0F1E");
    }
    syncControls();
  }

  function applyLang(lang) {
    var next = lang === "kn" ? "kn" : "en";
    root.setAttribute("data-lang", next);
    root.setAttribute("lang", next === "kn" ? "kn" : "en");
    writeStored(LANG_KEY, next);
    var pack = strings[next];
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      if (!key || pack[key] == null) {
        return;
      }
      if (el.getAttribute("data-i18n-html") === "true") {
        el.innerHTML = pack[key].replace(/\n/g, "<br />");
      } else {
        el.textContent = pack[key];
      }
    });

    var logo = document.querySelectorAll("[data-brand-logo]");
    logo.forEach(function (el) {
      el.setAttribute("src", assetBase() + (next === "kn" ? "imgs/logo-kn.svg" : "imgs/logo-en.svg"));
      if (el.closest(".nav-brand")) {
        el.setAttribute("alt", "");
      } else {
        el.setAttribute("alt", pack["home.title"] || "Bellandur Ganesha Utsava");
      }
    });

    if (document.body.getAttribute("data-page") === "resources") {
      document.title = pack["doc.resourcesTitle"];
    } else {
      document.title = pack["doc.title"];
    }

    syncControls();
    refreshDotLabels();
  }

  function syncControls() {
    var theme = currentTheme();
    var lang = currentLang();
    var themeBtn = document.getElementById("theme-toggle");
    if (themeBtn) {
      var pack = strings[lang];
      themeBtn.textContent = theme === "dark" ? pack["theme.toLight"] : pack["theme.toDark"];
      themeBtn.setAttribute(
        "aria-label",
        theme === "dark" ? "Switch to light theme" : "Switch to dark theme"
      );
    }
    document.querySelectorAll("[data-set-lang]").forEach(function (btn) {
      var value = btn.getAttribute("data-set-lang");
      btn.setAttribute("aria-pressed", value === lang ? "true" : "false");
    });
  }

  function refreshDotLabels() {
    var dotsRoot = document.getElementById("reel-dots");
    var reelsRoot = document.getElementById("reels");
    if (!dotsRoot || !reelsRoot) {
      return;
    }
    var lang = currentLang();
    var pack = strings[lang];
    var reels = reelsRoot.querySelectorAll(".reel");
    var buttons = dotsRoot.querySelectorAll("button");
    buttons.forEach(function (button, index) {
      var reel = reels[index];
      if (!reel) {
        return;
      }
      var labelKey = "dot." + (reel.dataset.label || "Home");
      var label = pack[labelKey] || reel.dataset.label || "section";
      button.setAttribute("aria-label", (lang === "kn" ? "ಹೋಗಿ: " : "Go to ") + label);
    });
  }

  function initControls() {
    applyTheme(readStored(THEME_KEY, currentTheme() || "dark"));
    applyLang(readStored(LANG_KEY, currentLang() || "en"));

    var themeBtn = document.getElementById("theme-toggle");
    if (themeBtn) {
      themeBtn.addEventListener("click", function () {
        applyTheme(currentTheme() === "dark" ? "light" : "dark");
      });
    }

    document.querySelectorAll("[data-set-lang]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        applyLang(btn.getAttribute("data-set-lang"));
      });
    });
  }

  function initReels() {
    var reelsRoot = document.getElementById("reels");
    var dotsRoot = document.getElementById("reel-dots");
    if (!reelsRoot || !dotsRoot) {
      return;
    }

    var reels = Array.prototype.slice.call(reelsRoot.querySelectorAll(".reel"));
    if (!reels.length) {
      return;
    }

    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function buildDots() {
      dotsRoot.innerHTML = "";
      reels.forEach(function (reel, index) {
        var button = document.createElement("button");
        button.type = "button";
        if (index === 0) {
          button.setAttribute("aria-current", "true");
        }
        button.addEventListener("click", function () {
          reel.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
        });
        dotsRoot.appendChild(button);
      });
      refreshDotLabels();
    }

    function setActive(index) {
      reels.forEach(function (reel, i) {
        reel.classList.toggle("is-active", i === index);
      });
      var buttons = dotsRoot.querySelectorAll("button");
      buttons.forEach(function (button, i) {
        if (i === index) {
          button.setAttribute("aria-current", "true");
        } else {
          button.removeAttribute("aria-current");
        }
      });

      var isAway = index > 0;
      document.body.classList.toggle("is-away-home", isAway);
      var navBrand = document.getElementById("nav-brand");
      if (navBrand) {
        navBrand.setAttribute("aria-hidden", isAway ? "false" : "true");
        if (isAway) {
          navBrand.removeAttribute("tabindex");
        } else {
          navBrand.setAttribute("tabindex", "-1");
        }
      }
    }

    function nearestIndex() {
      var mid = reelsRoot.scrollTop + reelsRoot.clientHeight / 2;
      var best = 0;
      var bestDist = Infinity;
      reels.forEach(function (reel, index) {
        var center = reel.offsetTop + reel.offsetHeight / 2;
        var dist = Math.abs(center - mid);
        if (dist < bestDist) {
          bestDist = dist;
          best = index;
        }
      });
      return best;
    }

    var ticking = false;
    reelsRoot.addEventListener(
      "scroll",
      function () {
        if (ticking) {
          return;
        }
        ticking = true;
        window.requestAnimationFrame(function () {
          setActive(nearestIndex());
          ticking = false;
        });
      },
      { passive: true }
    );

    buildDots();
    setActive(0);
  }

  initControls();
  initReels();
})();
