# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-10-14
"""
import time
import pytest
from selenium.webdriver.common.keys import Keys


# 几个测试样例
def test_connect_0(self):
    """
    官方快速入门的测试代码。如果没有任何输出，说明一切正常。
    """
    driver = self._driver
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()


def test_connect_1(self):
    """
    自己写的几个测试样例
    """
    driver = self._driver
    # 查看本机ip，查看代理是否起作用
    driver.get('http://httpbin.org/ip')
    print('1: ', driver.session_id)
    print('2: ', driver.page_source)
    print('3: ', driver.get_cookies())
    print(driver.title)


def test_connect_2(self):
    """
    自己写的几个测试样例
    """
    driver = self._driver
    driver.get('http://sahitest.com/demo/saveAs.htm')
    driver.find_element_by_xpath('//a[text()="testsaveas.zip"]').click()
    time.sleep(3)


if __name__ == '__main__':
    pytest.main()