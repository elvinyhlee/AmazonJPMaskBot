import os
import re
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from tg import send_text


chrome_driver_path = os.environ['CHROME_DRIVER_PATH']


class MaskBot:

    def __init__(self, targets):
        self.targets = targets
        self.offer_listing_url = 'https://www.amazon.co.jp/gp/offer-listing/'
        self.language_param = '?language=zh_CN'
        self.driver = webdriver.Chrome(chrome_driver_path)
        self.msg_record_time = {}
        # TODO (Elvin): sign in

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
                        msg = self._telegram_message(remark, price, url, product_name)
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

    # @staticmethod
    # def _add_to_cart(element):
    #     try:
    #         button = element.find_element_by_name('submit.addToCart')
    #         button.click()
    #     except NoSuchElementException:
    #         return False

    @staticmethod
    def _seller_is_amazon_jp(element):
        try:
            img = element.find_element_by_tag_name('img')
            return img.get_attribute('alt') == 'Amazon.co.jp'
        except NoSuchElementException:
            return False

    @staticmethod
    def _get_price_from_string(s):
        return int(re.sub('\D', '', s))  # e.g. ' ¥ 1000   ' -> 1000

    @staticmethod
    def _telegram_message(remark, price, url, product_name):
        return f'<b>有新貨🔥 {remark} ¥ {price} {url}</b>'

    def _not_repeated_reported(self, code):
        return (code not in self.msg_record_time or
                int((datetime.now() - self.msg_record_time[code]).total_seconds() // 60) > 10)  # reset in 10 minutes
