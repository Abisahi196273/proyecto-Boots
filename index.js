const puppeteer  = require("puppeteer")

(async() => {
    const browser = await puppeteer.launch({headless:False});
    const page = await browser.newPage();
    await page.goto("https://www.marinetraffic.com/en/ais/home/centerx:-12.0/centery:25.0/zoom:4");

    await page.waitForSelector("MuiGrid-root MuiGrid-item css-1wxaqej")
    await page.click("MuiGrid-root MuiGrid-item css-1wxaqej")

}
    )();