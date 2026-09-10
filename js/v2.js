/* Bellandur Ganesha Utsava v2.

   Three jobs: the language switch, the theme switch, and the phone accordions.
   No scroll engine. The sheet-stacking machinery this page started with was
   cut, so scroll position and anchor navigation are the browser's own.

   Kannada strings marked (approved) are lifted verbatim from the dictionary
   already shipping in js/main.js on the live site. The rest were written for
   this layout's copy, composed from that same approved vocabulary, and still
   want a native-speaker read before go-live. */
(function () {
  'use strict';

  var THEME_KEY = 'bgu-theme';   // shared with index.html
  var LANG_KEY = 'bgu-lang';     // shared with index.html
  var root = document.documentElement;

  /* ---- Strings --------------------------------------------------------- */

  var STRINGS = {
    en: {
      'skip': 'Skip to content',
      'nav.wordmark': 'Bellandur Ganesha Utsava',
      'nav.brandAria': 'Bellandur Ganesha Utsava, back to top',
      'nav.when': 'When',
      'nav.festival': 'The festival',
      'nav.photos': 'Photos',
      'nav.visarjan': 'Visarjan',
      'nav.visit': 'Visit',
      'nav.resources': 'Resources',
      'nav.donate': 'Donate',

      'hero.eyebrow': 'Bellandur · Bengaluru',
      'hero.title': 'Five days.<br />One street.<br /><em>Tenth year.</em>',
      'hero.altName': 'ಬೆಳ್ಳಂದೂರು ಗಣೇಶ ಉತ್ಸವ',
      'hero.dates': '14 to 18 September 2026',
      'hero.datesNote': 'Monday to Friday, free and open to everyone',
      'hero.sub': 'A community Ganesha festival in Bellandur, known for one of the tallest and richest idols in the area. Run by the neighbourhood, for the neighbourhood, for ten years.',
      'hero.ctaWhen': 'When is it',
      'hero.ctaDonate': 'Donate',
      'hero.markAlt': 'Bellandur Ganesha Utsava tenth year emblem',

      'when.eyebrow': 'When',
      'when.title': 'Five days, from Ganesh Chaturthi.',
      'when.lede': 'The shape is the same every year. Chaturthi opens it, three days of poojas carry it, and the visarjan closes it.',
      'when.noticeTitle': 'Dates for this year',
      'when.noticeBody': 'Monday 14 to Friday 18 September 2026, at the pandal near Shri Venkateshwara Swamy Temple. Any change is posted on Instagram and Facebook first.',
      'when.follow': 'Follow for updates',
      'when.d1num': 'Day 1',
      'when.d2num': 'Day 2',
      'when.d3num': 'Day 3',
      'when.d4num': 'Day 4',
      'when.d5num': 'Day 5',
      'when.d1title': 'Ganesh Chaturthi',
      'when.dPooja': 'Pooja and aarti',
      'when.d5title': 'Procession and visarjan',
      'when.d1date': 'Mon 14 Sep',
      'when.d2date': 'Tue 15 Sep',
      'when.d3date': 'Wed 16 Sep',
      'when.d4date': 'Thu 17 Sep',
      'when.d5date': 'Fri 18 Sep',
      'slot.d1t1': '11:30 am',
      'slot.d1w1': 'Ganapati Pratishthapana',
      'slot.d1s1': 'Prasadam through the rest of the day',
      'slot.d1t2': '5:00 pm',
      'slot.d1w2': 'Bharatanatyam',
      'slot.d1t3': '6:00 pm',
      'slot.d1w3': 'Ganga aarti',
      'slot.d1t4': '7:00 to 10:00 pm',
      'slot.d1w4': 'Grand orchestra',
      'slot.d2t1': '6:00 pm',
      'slot.d2w1': 'Aarti',
      'slot.d2s1': 'Followed by prasadam',
      'slot.d2t2': '7:00 to 10:00 pm',
      'slot.d2w2': 'Cine music and dance',
      'slot.d3t1': '6:00 pm',
      'slot.d3w1': 'Aarti',
      'slot.d3s1': 'Followed by prasadam',
      'slot.d3t2': '6:45 to 7:45 pm',
      'slot.d3w2': 'Classical devotional vocal',
      'slot.d3t3': '7:45 to 10:00 pm',
      'slot.d3w3': 'Bharatanatyam and western dance',
      'slot.d4t1': '6:00 pm',
      'slot.d4w1': 'Aarti',
      'slot.d4s1': 'Followed by prasadam',
      'slot.d4t2': '7:00 to 10:00 pm',
      'slot.d4w2': 'Grand orchestra',
      'slot.d5t1': '6:00 pm',
      'slot.d5w1': 'Aarti',
      'slot.d5s1': 'Followed by prasadam',
      'slot.d5t2': '6:00 pm onwards',
      'slot.d5w2': 'Grand procession and visarjan',

      'fact.yearNum': '10th',
      'fact.yearLabel': 'Year in Bellandur',
      'fact.daysNum': '5',
      'fact.daysLabel': 'Days of the festival',
      'fact.freeNum': 'Free',
      'fact.freeLabel': 'Open to everyone',

      'fest.eyebrow': 'The festival',
      'fest.title': 'The pooja is the point.',
      'fest.lede': 'The idol is why the crowds come, but the daily rituals are what the five days actually are. Nobody needs an invitation to stand in them.',
      'fest.cta': 'Plan your visit',
      'fest.aTitle': 'The idol',
      'fest.aText': 'One of the tallest and richest Ganesha idols in the area, installed in the pandal near Shri Venkateshwara Swamy Temple.',
      'fest.bTitle': 'Daily poojas and aarti',
      'fest.bText': 'Poojas, aarti and community rituals every day of the five, performed in front of the idol and open to everyone present.',
      'fest.cTitle': 'The neighbourhood',
      'fest.cText': 'For a week the pandal is a community space, and Bellandur turns up in large numbers across all five days.',
      'fest.dTitle': 'Seva',
      'fest.dText': 'Pooja arrangements, the idol and the community seva are handled by Sri Vinayaka Seva Mandali and Classic Boys, and funded by the area itself.',

      'photos.eyebrow': 'Photos and videos',
      'photos.title': 'Where the pictures live.',
      'photos.lede': 'The festival is documented as it happens, by the mandali and by everyone who attends. These are the three places it all ends up.',
      'photos.albumAria': 'Open the Bellandur Ganesha Utsava photo album',
      'photos.albumCap': 'The festival album',
      'photos.albumWhere': 'Google Photos',
      'photos.igAria': 'Bellandur Ganesha Utsava on Instagram',
      'photos.igCap': 'Day by day, as it happens',
      'photos.igWhere': 'Instagram',
      'photos.fbAria': 'Bellandur Ganesha Utsava videos on Facebook',
      'photos.fbCap': 'Procession and visarjan video',
      'photos.fbWhere': 'Facebook',

      'vis.eyebrow': 'The final day',
      'vis.title': 'Out on the street, one last time.',
      'vis.lede': 'The idol leaves the pandal and moves through Bellandur before the immersion. It is the single biggest crowd of the five days.',
      'vis.cta': 'Support the festival',
      'vis.aTitle': 'The procession',
      'vis.aText': 'A grand procession on day five, through the streets around the pandal.',
      'vis.bTitle': 'The visarjan',
      'vis.bText': 'The immersion that closes the festival, and draws the largest turnout of the week.',
      'vis.cTitle': 'Route and timing',
      'vis.cText': 'Friday 18 September, from 6:00 pm, after the evening aarti. The route is posted on Instagram and Facebook closer to the day.',
      'band.title': 'One mandali. One street. <span class="stroke">Ten years running.</span>',
      'band.text': 'Sri Vinayaka Seva Mandali and Classic Boys have run this festival in Bellandur for a decade. Same organisers, same neighbourhood, same five days.',

      'visit.eyebrow': 'Plan your visit',
      'visit.title': 'Before you come.',
      'visit.lede': 'The dates and the daily programme are set. Anything that changes is published on Instagram and Facebook first.',
      'visit.whereT': 'Where',
      'visit.whereB': 'Near Shri Venkateshwara Swamy Temple, 12th B Cross Rd, Bellandur, Bengaluru, Karnataka 560103.',
      'visit.gettingT': 'Getting there',
      'visit.gettingB': 'Bellandur is in east Bengaluru, on the Outer Ring Road. The pandal is in the lanes off 12th B Cross Road.',
      'visit.entryT': 'Entry',
      'visit.entryB': 'Free and open to everyone. There is no ticket, pass or registration.',
      'visit.timingsT': 'Timings',
      'visit.timingsB': 'Aarti is at 6:00 pm every day. Evening programmes run to about 10:00 pm. Day one opens at 11:30 am with the pratishthapana.',
      'visit.crowdsT': 'Crowds',
      'visit.crowdsB': 'Expect a large local turnout across all five days, and the heaviest of it around the procession.',
      'visit.updatedT': 'Stay updated',
      'visit.updatedB': 'Follow bellanduru_ganesha_utsava on Instagram, or the festival page on Facebook, for the procession route and anything that changes.',

      'about.eyebrow': 'The mandali',
      'about.title': 'Run by the neighbourhood.',
      'about.portraitAlt': 'Bellandur Ganesha Utsava Kannada emblem',
      'about.caption': 'Sri Vinayaka Seva Mandali & Classic Boys',
      'about.p1': 'Bellandur Ganesha Utsava is organised by Sri Vinayaka Seva Mandali and Classic Boys. This is the tenth year of the festival in Bellandur.',
      'about.p2': 'The pandal, the idol, the pooja arrangements and the community seva are all handled by the two groups and paid for by contributions from the area. There is no ticket, because the neighbourhood already funds it.',
      'about.p3': 'The pandal sits near Shri Venkateshwara Swamy Temple on 12th B Cross Road, and for five days every year it is the busiest spot in Bellandur.',

      'seva.eyebrow': 'Seva',
      'seva.title': 'Put something into the pooja.',
      'seva.lede': 'Support the mandali with pooja arrangements, the idol and community seva. Scan the QR to pay by UPI, or use the VPA directly from your bank app.',
      'seva.upi': 'UPI: 9845111817@kbl',
      'seva.org': 'Sri Vinayaka Seva Mandali',
      'seva.addr': 'Near Shri Venkateshwara Swamy Temple<br />12th B Cross Rd, Bellandur<br />Bengaluru, Karnataka 560103',
      'seva.qrAlt': 'UPI donation QR for Sri Vinayaka Seva Mandali',
      'seva.qrCap': 'Scan to pay',
      'seva.payCta': 'Pay by UPI',
      'vol.title': 'Volunteer',
      'vol.text': 'The five days are run by people from the area. If you want to help with the pandal, the poojas or the procession, reach the mandali through Instagram or Facebook.',
      'vol.cta': 'Reach the mandali',

      'foot.logoAlt': 'Bellandur Ganesha Utsava',
      'foot.tagline': 'Pooja · Aarti · Procession · Visarjan',
      'foot.ig': 'Instagram',
      'foot.fb': 'Facebook',
      'foot.res': 'Resources',
      'foot.copyright': '© 2026 Sri Vinayaka Seva Mandali & Classic Boys.',
      'pref.language': 'Language',
      'pref.theme': 'Theme',
      'pref.system': 'System',
      'pref.light': 'Light',
      'pref.dark': 'Dark',

      'doc.title': 'Bellandur Ganesha Utsava 2026 | 14 to 18 September, Bengaluru',
      'doc.desc': 'Bellandur Ganesha Utsava runs 14 to 18 September 2026 in Bellandur, Bengaluru. Daily aarti, evening music and dance, and the grand procession and visarjan on the 18th. Free and open to everyone.'
    },

    kn: {
      'skip': 'ವಿಷಯಕ್ಕೆ ಹೋಗಿ',
      'nav.wordmark': 'ಬೆಳ್ಳಂದೂರು ಗಣೇಶ ಉತ್ಸವ',
      'nav.brandAria': 'ಬೆಳ್ಳಂದೂರು ಗಣೇಶ ಉತ್ಸವ, ಮೇಲಕ್ಕೆ',
      'nav.when': 'ಯಾವಾಗ',
      'nav.festival': 'ಉತ್ಸವ',
      'nav.photos': 'ಚಿತ್ರಗಳು',
      'nav.visarjan': 'ವಿಸರ್ಜನೆ',
      'nav.visit': 'ಭೇಟಿ',
      'nav.resources': 'ಸಂಪನ್ಮೂಲಗಳು',
      'nav.donate': 'ದಾನ',

      'hero.eyebrow': 'ಬೆಳ್ಳಂದೂರು · ಬೆಂಗಳೂರು',
      'hero.title': 'ಐದು ದಿನ.<br />ಒಂದು ಬೀದಿ.<br /><em>೧೦ನೇ ವರ್ಷ.</em>',
      'hero.altName': 'Bellandur Ganesha Utsava',
      'hero.dates': '೧೪ ರಿಂದ ೧೮ ಸೆಪ್ಟೆಂಬರ್ ೨೦೨೬',
      'hero.datesNote': 'ಸೋಮವಾರದಿಂದ ಶುಕ್ರವಾರ, ಎಲ್ಲರಿಗೂ ಉಚಿತ ಪ್ರವೇಶ',
      'hero.sub': 'ಬೆಳ್ಳಂದೂರಿನ ಸಮುದಾಯ ಗಣೇಶ ಉತ್ಸವ. ಈ ಪ್ರದೇಶದ ಅತಿ ಎತ್ತರದ ಮತ್ತು ಸಂಪನ್ನ ಗಣೇಶ ಮೂರ್ತಿಗಳಲ್ಲಿ ಒಂದಕ್ಕೆ ಹೆಸರುವಾಸಿ. ಹತ್ತು ವರ್ಷಗಳಿಂದ ನೆರೆಹೊರೆಯವರಿಂದಲೇ ನಡೆಸಲಾಗುತ್ತಿದೆ.',
      'hero.ctaWhen': 'ಯಾವಾಗ',
      'hero.ctaDonate': 'ದಾನ',
      'hero.markAlt': 'ಬೆಳ್ಳಂದೂರು ಗಣೇಶ ಉತ್ಸವ ೧೦ನೇ ವರ್ಷದ ಲಾಂಛನ',

      'when.eyebrow': 'ಯಾವಾಗ',
      'when.title': 'ಗಣೇಶ ಚತುರ್ಥಿಯಿಂದ ಐದು ದಿನಗಳು.',
      'when.lede': 'ಪ್ರತಿ ವರ್ಷವೂ ಸ್ವರೂಪ ಒಂದೇ. ಚತುರ್ಥಿಯಿಂದ ಆರಂಭ, ಮೂರು ದಿನ ಪೂಜೆಗಳು, ವಿಸರ್ಜನೆಯೊಂದಿಗೆ ಸಮಾಪ್ತಿ.',
      'when.noticeTitle': 'ಈ ವರ್ಷದ ದಿನಾಂಕಗಳು',
      'when.noticeBody': 'ಸೋಮವಾರ ೧೪ ರಿಂದ ಶುಕ್ರವಾರ ೧೮ ಸೆಪ್ಟೆಂಬರ್ ೨೦೨೬, ಶ್ರೀ ವೆಂಕಟೇಶ್ವರ ಸ್ವಾಮಿ ದೇವಸ್ಥಾನದ ಬಳಿಯ ಪೆಂಡಾಲಿನಲ್ಲಿ. ಯಾವುದೇ ಬದಲಾವಣೆಯನ್ನು ಮೊದಲು Instagram ಮತ್ತು Facebook ನಲ್ಲಿ ಪ್ರಕಟಿಸಲಾಗುತ್ತದೆ.',
      'when.follow': 'ಮಾಹಿತಿಗಾಗಿ ಅನುಸರಿಸಿ',
      'when.d1num': 'ದಿನ ೧',
      'when.d2num': 'ದಿನ ೨',
      'when.d3num': 'ದಿನ ೩',
      'when.d4num': 'ದಿನ ೪',
      'when.d5num': 'ದಿನ ೫',
      'when.d1title': 'ಗಣೇಶ ಚತುರ್ಥಿ',
      'when.dPooja': 'ಪೂಜೆ ಮತ್ತು ಆರತಿ',
      'when.d5title': 'ಮೆರವಣಿಗೆ ಮತ್ತು ವಿಸರ್ಜನೆ',
      'when.d1date': 'ಸೋಮ ೧೪ ಸೆಪ್ಟೆಂಬರ್',
      'when.d2date': 'ಮಂಗಳ ೧೫ ಸೆಪ್ಟೆಂಬರ್',
      'when.d3date': 'ಬುಧ ೧೬ ಸೆಪ್ಟೆಂಬರ್',
      'when.d4date': 'ಗುರು ೧೭ ಸೆಪ್ಟೆಂಬರ್',
      'when.d5date': 'ಶುಕ್ರ ೧೮ ಸೆಪ್ಟೆಂಬರ್',
      'slot.d1t1': 'ಬೆಳಿಗ್ಗೆ ೧೧:೩೦',
      'slot.d1w1': 'ಗಣಪತಿ ಪ್ರತಿಷ್ಠಾಪನೆ',
      'slot.d1s1': 'ದಿನವಿಡೀ ಪ್ರಸಾದ ವಿತರಣೆ',
      'slot.d1t2': 'ಸಂಜೆ ೫:೦೦',
      'slot.d1w2': 'ಭರತನಾಟ್ಯ',
      'slot.d1t3': 'ಸಂಜೆ ೬:೦೦',
      'slot.d1w3': 'ಗಂಗಾ ಆರತಿ',
      'slot.d1t4': 'ಸಂಜೆ ೭:೦೦ ರಿಂದ ರಾತ್ರಿ ೧೦:೦೦',
      'slot.d1w4': 'ಭವ್ಯ ಆರ್ಕೆಸ್ಟ್ರಾ',
      'slot.d2t1': 'ಸಂಜೆ ೬:೦೦',
      'slot.d2w1': 'ಆರತಿ',
      'slot.d2s1': 'ನಂತರ ಪ್ರಸಾದ ವಿತರಣೆ',
      'slot.d2t2': 'ಸಂಜೆ ೭:೦೦ ರಿಂದ ರಾತ್ರಿ ೧೦:೦೦',
      'slot.d2w2': 'ಚಿತ್ರಗೀತೆ ಮತ್ತು ನೃತ್ಯ ಕಾರ್ಯಕ್ರಮ',
      'slot.d3t1': 'ಸಂಜೆ ೬:೦೦',
      'slot.d3w1': 'ಆರತಿ',
      'slot.d3s1': 'ನಂತರ ಪ್ರಸಾದ ವಿತರಣೆ',
      'slot.d3t2': 'ಸಂಜೆ ೬:೪೫ ರಿಂದ ೭:೪೫',
      'slot.d3w2': 'ಶಾಸ್ತ್ರೀಯ ಭಕ್ತಿಗೀತೆ ಗಾಯನ',
      'slot.d3t3': 'ಸಂಜೆ ೭:೪೫ ರಿಂದ ರಾತ್ರಿ ೧೦:೦೦',
      'slot.d3w3': 'ಭರತನಾಟ್ಯ ಮತ್ತು ಪಾಶ್ಚಾತ್ಯ ನೃತ್ಯ',
      'slot.d4t1': 'ಸಂಜೆ ೬:೦೦',
      'slot.d4w1': 'ಆರತಿ',
      'slot.d4s1': 'ನಂತರ ಪ್ರಸಾದ ವಿತರಣೆ',
      'slot.d4t2': 'ಸಂಜೆ ೭:೦೦ ರಿಂದ ರಾತ್ರಿ ೧೦:೦೦',
      'slot.d4w2': 'ಭವ್ಯ ಆರ್ಕೆಸ್ಟ್ರಾ',
      'slot.d5t1': 'ಸಂಜೆ ೬:೦೦',
      'slot.d5w1': 'ಆರತಿ',
      'slot.d5s1': 'ನಂತರ ಪ್ರಸಾದ ವಿತರಣೆ',
      'slot.d5t2': 'ಸಂಜೆ ೬:೦೦ ರಿಂದ',
      'slot.d5w2': 'ಭವ್ಯ ಮೆರವಣಿಗೆ ಮತ್ತು ವಿಸರ್ಜನೆ',

      'fact.yearNum': '೧೦ನೇ',
      'fact.yearLabel': 'ಬೆಳ್ಳಂದೂರಿನಲ್ಲಿ ವರ್ಷ',
      'fact.daysNum': '೫',
      'fact.daysLabel': 'ಉತ್ಸವದ ದಿನಗಳು',
      'fact.freeNum': 'ಉಚಿತ',
      'fact.freeLabel': 'ಎಲ್ಲರಿಗೂ ಮುಕ್ತ',

      'fest.eyebrow': 'ಉತ್ಸವ',
      'fest.title': 'ಪೂಜೆಯೇ ಮುಖ್ಯ.',
      'fest.lede': 'ಮೂರ್ತಿಯಿಂದಾಗಿ ಜನ ಬರುತ್ತಾರೆ, ಆದರೆ ಈ ಐದು ದಿನಗಳ ನಿಜವಾದ ಸಾರ ದೈನಂದಿನ ಆಚರಣೆಗಳು. ಅವುಗಳಲ್ಲಿ ಪಾಲ್ಗೊಳ್ಳಲು ಆಮಂತ್ರಣ ಬೇಕಿಲ್ಲ.',
      'fest.cta': 'ಭೇಟಿಯ ಯೋಜನೆ',
      'fest.aTitle': 'ಮೂರ್ತಿ',
      'fest.aText': 'ಈ ಪ್ರದೇಶದ ಅತಿ ಎತ್ತರದ ಮತ್ತು ಸಂಪನ್ನ ಗಣೇಶ ಮೂರ್ತಿಗಳಲ್ಲಿ ಒಂದು, ಶ್ರೀ ವೆಂಕಟೇಶ್ವರ ಸ್ವಾಮಿ ದೇವಸ್ಥಾನದ ಹತ್ತಿರದ ಪಂದಾಲಿನಲ್ಲಿ ಪ್ರತಿಷ್ಠಾಪಿಸಲಾಗಿದೆ.',
      'fest.bTitle': 'ದೈನಂದಿನ ಪೂಜೆ ಮತ್ತು ಆರತಿ',
      'fest.bText': 'ಐದೂ ದಿನ ಪೂಜೆ, ಆರತಿ ಮತ್ತು ಸಮುದಾಯ ಆಚರಣೆಗಳು, ಮೂರ್ತಿಯ ಮುಂದೆ, ಹಾಜರಿರುವ ಎಲ್ಲರಿಗೂ ಮುಕ್ತ.',
      'fest.cTitle': 'ನೆರೆಹೊರೆ',
      'fest.cText': 'ಒಂದು ವಾರ ಪಂದಾಲ್ ಸಮುದಾಯದ ಸ್ಥಳವಾಗುತ್ತದೆ, ಮತ್ತು ಐದೂ ದಿನ ಬೆಳ್ಳಂದೂರು ದೊಡ್ಡ ಸಂಖ್ಯೆಯಲ್ಲಿ ಸೇರುತ್ತದೆ.',
      'fest.dTitle': 'ಸೇವೆ',
      'fest.dText': 'ಪೂಜಾ ವ್ಯವಸ್ಥೆ, ಮೂರ್ತಿ ಮತ್ತು ಸಮುದಾಯ ಸೇವೆಯನ್ನು ಶ್ರೀ ವಿನಾಯಕ ಸೇವಾ ಮಂಡಲಿ ಮತ್ತು ಕ್ಲಾಸಿಕ್ ಬಾಯ್ಸ್ ನಿರ್ವಹಿಸುತ್ತಾರೆ, ಮತ್ತು ಈ ಪ್ರದೇಶವೇ ಹಣ ಒದಗಿಸುತ್ತದೆ.',

      'photos.eyebrow': 'ಫೋಟೋ ಮತ್ತು ವೀಡಿಯೊಗಳು',
      'photos.title': 'ಚಿತ್ರಗಳು ಎಲ್ಲಿವೆ.',
      'photos.lede': 'ಉತ್ಸವ ನಡೆಯುತ್ತಿರುವಂತೆಯೇ ಮಂಡಲಿ ಮತ್ತು ಬಂದವರೆಲ್ಲ ದಾಖಲಿಸುತ್ತಾರೆ. ಎಲ್ಲವೂ ಸೇರುವ ಮೂರು ಸ್ಥಳಗಳು ಇವು.',
      'photos.albumAria': 'ಬೆಳ್ಳಂದೂರು ಗಣೇಶ ಉತ್ಸವ ಫೋಟೋ ಆಲ್ಬಮ್ ತೆರೆಯಿರಿ',
      'photos.albumCap': 'ಉತ್ಸವದ ಫೋಟೋ ಆಲ್ಬಮ್',
      'photos.albumWhere': 'Google Photos',
      'photos.igAria': 'Instagram ನಲ್ಲಿ ಬೆಳ್ಳಂದೂರು ಗಣೇಶ ಉತ್ಸವ',
      'photos.igCap': 'ದಿನದಿಂದ ದಿನಕ್ಕೆ, ನಡೆಯುತ್ತಿರುವಂತೆ',
      'photos.igWhere': 'Instagram',
      'photos.fbAria': 'Facebook ನಲ್ಲಿ ಬೆಳ್ಳಂದೂರು ಗಣೇಶ ಉತ್ಸವ ವೀಡಿಯೊಗಳು',
      'photos.fbCap': 'ಮೆರವಣಿಗೆ ಮತ್ತು ವಿಸರ್ಜನೆ ವೀಡಿಯೊ',
      'photos.fbWhere': 'Facebook',

      'vis.eyebrow': 'ಕೊನೆಯ ದಿನ',
      'vis.title': 'ಕೊನೆಯ ಬಾರಿ ಬೀದಿಯಲ್ಲಿ.',
      'vis.lede': 'ಮೂರ್ತಿ ಪಂದಾಲಿನಿಂದ ಹೊರಟು ವಿಸರ್ಜನೆಗೆ ಮೊದಲು ಬೆಳ್ಳಂದೂರಿನಲ್ಲಿ ಸಾಗುತ್ತದೆ. ಐದು ದಿನಗಳಲ್ಲಿ ಇದೇ ಅತಿ ದೊಡ್ಡ ಜನಸಂದಣಿ.',
      'vis.cta': 'ಉತ್ಸವಕ್ಕೆ ಬೆಂಬಲ',
      'vis.aTitle': 'ಮೆರವಣಿಗೆ',
      'vis.aText': 'ಐದನೇ ದಿನ ಪಂದಾಲಿನ ಸುತ್ತಿನ ಬೀದಿಗಳಲ್ಲಿ ವಿಶಾಲ ಮೆರವಣಿಗೆ.',
      'vis.bTitle': 'ವಿಸರ್ಜನೆ',
      'vis.bText': 'ಉತ್ಸವವನ್ನು ಮುಗಿಸುವ ವಿಸರ್ಜನೆ, ವಾರದ ಅತಿ ದೊಡ್ಡ ಭಾಗವಹಿಸುವಿಕೆ.',
      'vis.cTitle': 'ಮಾರ್ಗ ಮತ್ತು ಸಮಯ',
      'vis.cText': 'ಶುಕ್ರವಾರ ೧೮ ಸೆಪ್ಟೆಂಬರ್, ಸಂಜೆ ಆರತಿಯ ನಂತರ ಸಂಜೆ ೬:೦೦ ರಿಂದ. ಮಾರ್ಗವನ್ನು ದಿನದ ಹತ್ತಿರ Instagram ಮತ್ತು Facebook ನಲ್ಲಿ ಪ್ರಕಟಿಸಲಾಗುತ್ತದೆ.',
      'band.title': 'ಒಂದು ಮಂಡಲಿ. ಒಂದು ಬೀದಿ. <span class="stroke">ಹತ್ತು ವರ್ಷಗಳಿಂದ.</span>',
      'band.text': 'ಶ್ರೀ ವಿನಾಯಕ ಸೇವಾ ಮಂಡಲಿ ಮತ್ತು ಕ್ಲಾಸಿಕ್ ಬಾಯ್ಸ್ ಒಂದು ದಶಕದಿಂದ ಬೆಳ್ಳಂದೂರಿನಲ್ಲಿ ಈ ಉತ್ಸವವನ್ನು ನಡೆಸುತ್ತಿದ್ದಾರೆ. ಅದೇ ಆಯೋಜಕರು, ಅದೇ ನೆರೆಹೊರೆ, ಅದೇ ಐದು ದಿನಗಳು.',

      'visit.eyebrow': 'ಭೇಟಿಯ ಯೋಜನೆ',
      'visit.title': 'ಬರುವ ಮೊದಲು.',
      'visit.lede': 'ದಿನಾಂಕಗಳು ಮತ್ತು ದೈನಂದಿನ ಕಾರ್ಯಕ್ರಮ ನಿಗದಿಯಾಗಿದೆ. ಬದಲಾವಣೆಗಳನ್ನು ಮೊದಲು Instagram ಮತ್ತು Facebook ನಲ್ಲಿ ಪ್ರಕಟಿಸಲಾಗುತ್ತದೆ.',
      'visit.whereT': 'ಸ್ಥಳ',
      'visit.whereB': 'ಶ್ರೀ ವೆಂಕಟೇಶ್ವರ ಸ್ವಾಮಿ ದೇವಸ್ಥಾನದ ಹತ್ತಿರ, ೧೨ನೇ ಬಿ ಕ್ರಾಸ್ ರಸ್ತೆ, ಬೆಳ್ಳಂದೂರು, ಬೆಂಗಳೂರು, ಕರ್ನಾಟಕ ೫೬೦೧೦೩',
      'visit.gettingT': 'ತಲುಪುವುದು ಹೇಗೆ',
      'visit.gettingB': 'ಬೆಳ್ಳಂದೂರು ಪೂರ್ವ ಬೆಂಗಳೂರಿನಲ್ಲಿ, ಹೊರ ವರ್ತುಲ ರಸ್ತೆಯಲ್ಲಿದೆ. ಪಂದಾಲ್ ೧೨ನೇ ಬಿ ಕ್ರಾಸ್ ರಸ್ತೆಯ ಒಳಗಿನ ಬೀದಿಗಳಲ್ಲಿದೆ.',
      'visit.entryT': 'ಪ್ರವೇಶ',
      'visit.entryB': 'ಉಚಿತ ಮತ್ತು ಎಲ್ಲರಿಗೂ ಮುಕ್ತ. ಟಿಕೆಟ್, ಪಾಸ್ ಅಥವಾ ನೋಂದಣಿ ಇಲ್ಲ.',
      'visit.timingsT': 'ಸಮಯ',
      'visit.timingsB': 'ಪ್ರತಿ ದಿನ ಸಂಜೆ ೬:೦೦ ಕ್ಕೆ ಆರತಿ. ಸಂಜೆಯ ಕಾರ್ಯಕ್ರಮಗಳು ರಾತ್ರಿ ೧೦:೦೦ ರವರೆಗೆ. ಮೊದಲ ದಿನ ಬೆಳಿಗ್ಗೆ ೧೧:೩೦ ಕ್ಕೆ ಪ್ರತಿಷ್ಠಾಪನೆಯಿಂದ ಆರಂಭ.',
      'visit.crowdsT': 'ಜನಸಂದಣಿ',
      'visit.crowdsB': 'ಐದೂ ದಿನ ದೊಡ್ಡ ಸ್ಥಳೀಯ ಭಾಗವಹಿಸುವಿಕೆ ನಿರೀಕ್ಷಿಸಿ, ಮೆರವಣಿಗೆಯ ಸಮಯದಲ್ಲಿ ಅತಿ ಹೆಚ್ಚು.',
      'visit.updatedT': 'ಮಾಹಿತಿ ಪಡೆಯಿರಿ',
      'visit.updatedB': 'ಮೆರವಣಿಗೆಯ ಮಾರ್ಗ ಮತ್ತು ಯಾವುದೇ ಬದಲಾವಣೆಗಳಿಗಾಗಿ Instagram ನಲ್ಲಿ bellanduru_ganesha_utsava ಅಥವಾ Facebook ಪುಟವನ್ನು ಅನುಸರಿಸಿ.',

      'about.eyebrow': 'ಮಂಡಲಿ',
      'about.title': 'ನೆರೆಹೊರೆಯಿಂದಲೇ ನಡೆಸಲಾಗುತ್ತದೆ.',
      'about.portraitAlt': 'ಬೆಳ್ಳಂದೂರು ಗಣೇಶ ಉತ್ಸವ ಕನ್ನಡ ಲಾಂಛನ',
      'about.caption': 'ಶ್ರೀ ವಿನಾಯಕ ಸೇವಾ ಮಂಡಲಿ ಮತ್ತು ಕ್ಲಾಸಿಕ್ ಬಾಯ್ಸ್',
      'about.p1': 'ಬೆಳ್ಳಂದೂರು ಗಣೇಶ ಉತ್ಸವವನ್ನು ಶ್ರೀ ವಿನಾಯಕ ಸೇವಾ ಮಂಡಲಿ ಮತ್ತು ಕ್ಲಾಸಿಕ್ ಬಾಯ್ಸ್ ಆಯೋಜಿಸುತ್ತಾರೆ. ಇದು ಬೆಳ್ಳಂದೂರಿನಲ್ಲಿ ಉತ್ಸವದ ೧೦ನೇ ವರ್ಷ.',
      'about.p2': 'ಪಂದಾಲ್, ಮೂರ್ತಿ, ಪೂಜಾ ವ್ಯವಸ್ಥೆ ಮತ್ತು ಸಮುದಾಯ ಸೇವೆ ಎಲ್ಲವನ್ನೂ ಈ ಎರಡು ಗುಂಪುಗಳು ನಿರ್ವಹಿಸುತ್ತವೆ, ಮತ್ತು ಈ ಪ್ರದೇಶದ ದೇಣಿಗೆಯಿಂದ ನಡೆಯುತ್ತದೆ. ನೆರೆಹೊರೆಯೇ ಹಣ ಒದಗಿಸುವುದರಿಂದ ಟಿಕೆಟ್ ಇಲ್ಲ.',
      'about.p3': 'ಪಂದಾಲ್ ೧೨ನೇ ಬಿ ಕ್ರಾಸ್ ರಸ್ತೆಯಲ್ಲಿ ಶ್ರೀ ವೆಂಕಟೇಶ್ವರ ಸ್ವಾಮಿ ದೇವಸ್ಥಾನದ ಹತ್ತಿರ ಇದೆ, ಮತ್ತು ಪ್ರತಿ ವರ್ಷ ಐದು ದಿನ ಅದು ಬೆಳ್ಳಂದೂರಿನ ಅತಿ ಜನನಿಬಿಡ ಸ್ಥಳ.',

      'seva.eyebrow': 'ಸೇವೆ',
      'seva.title': 'ಪೂಜೆಗೆ ನಿಮ್ಮ ಕೊಡುಗೆ.',
      'seva.lede': 'ಪೂಜಾ ವ್ಯವಸ್ಥೆ, ಮೂರ್ತಿ ಮತ್ತು ಸಮುದಾಯ ಸೇವೆಗೆ ಮಂಡಲಿಗೆ ಬೆಂಬಲಿಸಿ. UPI ಮೂಲಕ ಪಾವತಿಸಲು QR ಸ್ಕ್ಯಾನ್ ಮಾಡಿ, ಅಥವಾ ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಆ್ಯಪ್‌ನಲ್ಲಿ VPA ಬಳಸಿ.',
      'seva.upi': 'UPI: 9845111817@kbl',
      'seva.org': 'ಶ್ರೀ ವಿನಾಯಕ ಸೇವಾ ಮಂಡಲಿ',
      'seva.addr': 'ಶ್ರೀ ವೆಂಕಟೇಶ್ವರ ಸ್ವಾಮಿ ದೇವಸ್ಥಾನದ ಹತ್ತಿರ<br />೧೨ನೇ ಬಿ ಕ್ರಾಸ್ ರಸ್ತೆ, ಬೆಳ್ಳಂದೂರು<br />ಬೆಂಗಳೂರು, ಕರ್ನಾಟಕ ೫೬೦೧೦೩',
      'seva.qrAlt': 'ಶ್ರೀ ವಿನಾಯಕ ಸೇವಾ ಮಂಡಲಿ UPI ದಾನ QR',
      'seva.qrCap': 'ಪಾವತಿಸಲು ಸ್ಕ್ಯಾನ್ ಮಾಡಿ',
      'seva.payCta': 'UPI ಮೂಲಕ ಪಾವತಿಸಿ',
      'vol.title': 'ಸ್ವಯಂಸೇವಕರಾಗಿ',
      'vol.text': 'ಈ ಐದು ದಿನಗಳನ್ನು ಈ ಪ್ರದೇಶದ ಜನರೇ ನಡೆಸುತ್ತಾರೆ. ಪಂದಾಲ್, ಪೂಜೆ ಅಥವಾ ಮೆರವಣಿಗೆಯಲ್ಲಿ ಸಹಾಯ ಮಾಡಲು Instagram ಅಥವಾ Facebook ಮೂಲಕ ಮಂಡಲಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.',
      'vol.cta': 'ಮಂಡಲಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ',

      'foot.logoAlt': 'ಬೆಳ್ಳಂದೂರು ಗಣೇಶ ಉತ್ಸವ',
      'foot.tagline': 'ಪೂಜೆ · ಆರತಿ · ಮೆರವಣಿಗೆ · ವಿಸರ್ಜನೆ',
      'foot.ig': 'Instagram',
      'foot.fb': 'Facebook',
      'foot.res': 'ಸಂಪನ್ಮೂಲಗಳು',
      'foot.copyright': '© ೨೦೨೬ ಶ್ರೀ ವಿನಾಯಕ ಸೇವಾ ಮಂಡಲಿ ಮತ್ತು ಕ್ಲಾಸಿಕ್ ಬಾಯ್ಸ್.',
      'pref.language': 'ಭಾಷೆ',
      'pref.theme': 'ಥೀಮ್',
      'pref.system': 'ಸಾಧನದಂತೆ',
      'pref.light': 'ಬೆಳಕು',
      'pref.dark': 'ಕತ್ತಲೆ',

      'doc.title': 'ಬೆಳ್ಳಂದೂರು ಗಣೇಶ ಉತ್ಸವ ೨೦೨೬ | ೧೪ ರಿಂದ ೧೮ ಸೆಪ್ಟೆಂಬರ್, ಬೆಂಗಳೂರು',
      'doc.desc': 'ಬೆಳ್ಳಂದೂರು ಗಣೇಶ ಉತ್ಸವ ೨೦೨೬ ಸೆಪ್ಟೆಂಬರ್ ೧೪ ರಿಂದ ೧೮ ರವರೆಗೆ ಬೆಂಗಳೂರಿನ ಬೆಳ್ಳಂದೂರಿನಲ್ಲಿ. ದೈನಂದಿನ ಆರತಿ, ಸಂಜೆಯ ಸಂಗೀತ ಮತ್ತು ನೃತ್ಯ, ೧೮ ರಂದು ಭವ್ಯ ಮೆರವಣಿಗೆ ಮತ್ತು ವಿಸರ್ಜನೆ. ಎಲ್ಲರಿಗೂ ಉಚಿತ ಪ್ರವೇಶ.'
    }
  };

  /* ---- Language -------------------------------------------------------- */

  var lang = 'en';

  function applyLang(next) {
    lang = STRINGS[next] ? next : 'en';
    var dict = STRINGS[lang];
    var other = lang === 'en' ? 'kn' : 'en';

    root.setAttribute('lang', lang);
    root.setAttribute('data-lang', lang);

    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var v = dict[el.getAttribute('data-i18n')];
      if (v != null) el.textContent = v;
    });

    /* innerHTML only for the three strings that carry markup of their own (a
       line break, an <em>, the highlighted span). Every value comes from the
       dictionary above, never from anything a visitor can supply. */
    document.querySelectorAll('[data-i18n-html]').forEach(function (el) {
      var v = dict[el.getAttribute('data-i18n-html')];
      if (v != null) el.innerHTML = v;
    });

    document.querySelectorAll('[data-i18n-alt]').forEach(function (el) {
      var v = dict[el.getAttribute('data-i18n-alt')];
      if (v != null) el.setAttribute('alt', v);
    });

    document.querySelectorAll('[data-i18n-aria]').forEach(function (el) {
      var v = dict[el.getAttribute('data-i18n-aria')];
      if (v != null) el.setAttribute('aria-label', v);
    });

    /* This one holds the name in the language the page is NOT in, so its own
       lang attribute has to move the opposite way for correct shaping and
       for screen readers. */
    document.querySelectorAll('[data-i18n-altlang]').forEach(function (el) {
      el.setAttribute('lang', other);
    });

    if (dict['doc.title']) document.title = dict['doc.title'];
    var desc = document.querySelector('meta[name="description"]');
    if (desc && dict['doc.desc']) desc.setAttribute('content', dict['doc.desc']);

    document.querySelectorAll('[data-set-lang]').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-set-lang') === lang ? 'true' : 'false');
    });

    try { localStorage.setItem(LANG_KEY, lang); } catch (e) {}
  }

  /* ---- Theme ----------------------------------------------------------- */
  /* Three states. "system" removes the attribute entirely so the stylesheet's
     prefers-color-scheme query decides; light and dark pin it. */

  var systemDark = window.matchMedia('(prefers-color-scheme: dark)');
  var themeMeta = document.querySelector('meta[name="theme-color"]');

  function paintMeta() {
    if (!themeMeta) return;
    var dark = root.getAttribute('data-theme') === 'dark' ||
      (!root.hasAttribute('data-theme') && systemDark.matches);
    themeMeta.setAttribute('content', dark ? '#1a0508' : '#fff8ec');
  }

  function applyTheme(mode) {
    if (mode !== 'light' && mode !== 'dark') mode = 'system';
    if (mode === 'system') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', mode);

    document.querySelectorAll('[data-set-theme]').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-set-theme') === mode ? 'true' : 'false');
    });

    paintMeta();
    try { localStorage.setItem(THEME_KEY, mode); } catch (e) {}
  }

  /* While on "system", follow the device if it changes under us. */
  systemDark.addEventListener('change', function () {
    if (!root.hasAttribute('data-theme')) paintMeta();
  });

  /* ---- Wire up --------------------------------------------------------- */

  var storedLang = 'en', storedTheme = 'system';
  try {
    storedLang = localStorage.getItem(LANG_KEY) || 'en';
    storedTheme = localStorage.getItem(THEME_KEY) || 'system';
  } catch (e) {}

  applyLang(storedLang);
  applyTheme(storedTheme);

  document.querySelectorAll('[data-set-lang]').forEach(function (b) {
    b.addEventListener('click', function () { applyLang(b.getAttribute('data-set-lang')); });
  });
  document.querySelectorAll('[data-set-theme]').forEach(function (b) {
    b.addEventListener('click', function () { applyTheme(b.getAttribute('data-set-theme')); });
  });

  /* ---- Phone: detail rows collapse ------------------------------------- */

  var mqPhone = window.matchMedia('(max-width: 640px)');
  var rows = Array.prototype.slice.call(document.querySelectorAll('.row'));

  function toggleRow(row) {
    var open = row.classList.toggle('is-open');
    row.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  /* Only interactive at phone widths, so the button semantics come and go
     with the media query rather than sitting in the markup. */
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
