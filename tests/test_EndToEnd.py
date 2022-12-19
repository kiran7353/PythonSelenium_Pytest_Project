from reusableMethods.BaseClass import *
from pageObjects.HomePage import *


class TestOne(BaseClass):

    def test_endToend(self):
        log = self.getLogger()
        homePage = HomePage(self.driver)
        checkout = homePage.shopItems()
        log.info("getting all the card titles")
        cards = checkout.getCardTitles()
        i = -1
        for card in cards:
            i = i + 1
            cardText = card.text
            log.info(cardText)
            if cardText == "Blackberry":
                checkout.getCardFooter()[i].click()

        self.driver.find_element_by_css_selector("a[class*='btn-primary']").click()

        confirmPage = checkout.checkOutItems()
        log.info("Entering country name as ind")
        self.driver.find_element_by_id("country").send_keys("ind")
        self.verifyLinkPresence("India")

        self.driver.find_element_by_link_text("India").click()
        self.driver.find_element_by_xpath("//div[@class='checkbox checkbox-primary']").click()
        self.driver.find_element_by_css_selector("[type='submit']").click()
        textMatch = self.driver.find_element_by_css_selector("[class*='alert-success']").text
        log.info("Text received from application is " + textMatch)

        assert ("Success! Thank you!" in textMatch)
