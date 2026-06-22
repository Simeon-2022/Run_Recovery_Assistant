const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const url = process.env.TARGET_URL || 'file://' + __dirname + '/index.html';

  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });

  try {
    const resp = await page.goto(url, { waitUntil: 'networkidle' });
    console.log('Loaded', url, 'status', resp ? resp.status() : 'file');

    // Attempt to fill a basic form if present
    try {
      await page.fill('input[name="duration"]', '30');
      await page.fill('input[name="mileage"]', '5');
      await page.fill('input[name="pace"]', '5.5');
    } catch (e) {
      // not all fields exist; ignore
    }

    // Try clicking a submit button
    const submit = await page.$('button[type="submit"]');
    if (submit) await submit.click();

    // Wait briefly for UI updates
    await page.waitForTimeout(800);

    if (consoleErrors.length) {
      console.error('Console errors detected:');
      consoleErrors.forEach(e => console.error(e));
      process.exitCode = 2;
    } else {
      console.log('No console errors detected.');
    }
  } catch (err) {
    console.error('Smoke test failed:', err);
    process.exitCode = 1;
  } finally {
    await browser.close();
  }
})();
