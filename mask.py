import os
import re
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randint
from tg import send_text


chrome_driver_path = os.environ['CHROME_DRIVER_PATH']
chrome_options = Options()
chrome_options.add_argument("--headless")


class MaskBot:

    def __init__(self, targets, email=None, password=None):
        self.targets = targets
        self.email = email
        self.password = password
        self.msg_record_time = {}

        self.offer_listing_url = 'https://www.amazon.co.jp/gp/offer-listing/'
        self.log_in_url = 'https://www.amazon.co.jp/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=jpflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.jp%2Fref%3Dnav_signin&switch_account='
        self.language_param = '?language=zh_CN'

        self.driver = webdriver.Chrome(chrome_driver_path, chrome_options=chrome_options)

    def scan(self):
        for code, remark in self.targets:
            url = self.offer_listing_url + code + self.language_param
            self.driver.get(url)

            try:
                product_name = self.driver.find_element_by_id('olpProductDetails').find_element_by_tag_name('h1').text
                print(f'[{remark}] {product_name}')  # logging

                offers = self.driver.find_elements_by_css_selector('div.a-row.a-spacing-mini.olpOffer')

                for offer in offers:
                    price = self._get_price_from_string(offer.find_element_by_css_selector(
                        'span.a-size-large.a-color-price.olpOfferPrice.a-text-bold'
                    ).text)
                    seller = offer.find_element_by_css_selector('div.a-column.a-span2.olpSellerColumn')

                    if self._seller_is_amazon_jp(seller) and self._not_repeated_reported(code):
                        self.msg_record_time[code] = datetime.now()
                        msg = self._telegram_message(remark, price, url)
                        send_text(msg)

                        # TODO (Elvin): add to cart
                        # self._add_to_cart(offer)

                        print(f'有新貨🔥 {product_name} {remark} ¥ {price} {url}')  # logging
                        break

            except NoSuchElementException:
                print('no offering')

    def repeated_scan(self):
        while True:
            self.scan()

    def close(self):
        self.driver.close()

    def login(self):
        if not (self.email and self.password):
            raise ValueError('Can\'t login without email or password')
        try:
            self.driver.get(self.log_in_url)
            self.driver.find_element_by_id('ap_email').send_keys(self.email)
            sleep(randint(10, 30))
            self.driver.find_element_by_id('continue').click()
            sleep(randint(10, 30))
            self.driver.find_element_by_id('ap_password').send_keys(self.password)
            sleep(randint(10, 30))
            self.driver.find_element_by_id('signInSubmit').click()
            print('Successfully Login ')
            sleep(randint(10, 30))
        except NoSuchElementException:
            print('Can\'t login, please try again')

    @staticmethod
    def _add_to_cart(element):
        try:
            button = element.find_element_by_name('submit.addToCart')
            button.click()
        except NoSuchElementException:
            print('can\'t add to cart')

    @staticmethod
    def _seller_is_amazon_jp(element) -> bool:
        try:
            img = element.find_element_by_tag_name('img')
            return img.get_attribute('alt') == 'Amazon.co.jp'
        except NoSuchElementException:
            return False

    @staticmethod
    def _get_price_from_string(s: str) -> int:
        return int(re.sub('\D', '', s))  # e.g. ' ¥ 1000   ' -> 1000

    @staticmethod
    def _telegram_message(remark: str, price: int, url: str) -> str:
        return f'<b>有新貨🔥 {remark} ¥ {price} {url}</b>'

    def _not_repeated_reported(self, code: str) -> bool:
        return (code not in self.msg_record_time or
                int((datetime.now() - self.msg_record_time[code]).total_seconds() // 60) > 10)  # reset in 10 minutes
