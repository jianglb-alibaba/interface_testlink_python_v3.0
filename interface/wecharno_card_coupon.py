#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laiyu'

import json

from globalpkg.log import logger
from globalpkg.global_var import cookie
from globalpkg.global_var import global_serial
from globalpkg.global_var import global_openId
from globalpkg.global_var import saofudb
from unittesttestcase import MyUnittestTestCase
from htmlparser import  MyHTMLParser

__all__ = ['GetInCoupon']

# 领取卡券接口
class GetInCoupon(MyUnittestTestCase):
    card_code = '' # coupon_weixin_customer.serial
    cash_reduce_cost = 0 # 代金券抵扣金额
    discount = 0         # 折扣券优惠的折扣 = 100-折扣券折扣 * 10

    def setUp(self):
        # 判断代金券\折扣券是否有剩余库存，是否下架
        logger.info(self.url)
        str_list = self.url.split('/')
        coupon_serial = str_list[3]
        query = 'SELECT sku_quantity, listing FROM base_info WHERE serial = %s'
        data = (coupon_serial,)
        result = saofudb.select_one_record(query, data)
        sku_quantity = result[0]

        ison = result[1]
        if sku_quantity == 1:
            query = 'UPDATE base_info SET sku_quantity = 100000000'
            saofudb.execute_update(query)
        if ison == 0:
            query = 'UPDATE base_info SET listing = 1'
            saofudb.execute_update(query)

    # 免费领取代金券、折扣券
    def test_get_in_coupon(self):
        headers = cookie
        headers.update(cookie)
        self.http.set_header(headers)

        str_list = self.url.split('/')
        logger.info(str_list)
        coupon_serial = str_list[3]

        # 记录初始库存
        query = 'SELECT sku_quantity FROM base_info WHERE serial = %s';
        data = (coupon_serial,)
        result = saofudb.select_one_record(query, data)
        sku_quantity_old = result[0]

        logger.info('正在发起POST请求...')
        self.url = self.url.replace('[global_openId]', global_openId)
        self.params = self.params.encode('utf-8')
        response = self.http.post(self.url, self.params)
        response = response[0].decode('utf-8')
        response = json.loads(response)

        logger.info('正在解析返回结果:%s' % response)

        GetInCoupon.card_code = response['cardCode'] # 供其它支付使用

        query = 'SELECT title, sub_title, notice, description, use_limit, date_info_type, sku_quantity, detail_txt, service_phone, id ' \
                'FROM base_info WHERE serial = %s'
        data = (coupon_serial,)
        result = saofudb.select_one_record(query, data)
        self.expected_result['title'] = result[0]
        self.expected_result['subTitle'] = result[1]
        self.expected_result['notice'] = result[2]
        self.expected_result['description'] = result[3]
        self.expected_result['useLimit'] = result[4]
        self.expected_result['dateInfoType'] = result[5]
        self.expected_result['skuQuantity'] = sku_quantity_old - 1
        sku_quantity_new = result[6]
        self.expected_result['detailTxt'] = result[7]
        self.expected_result['servicePhone'] = result[8]
        base_info_Id = result[9]

        query = 'SELECT cash_least_cost, cash_reduce_cost,discount  FROM coupon_weixin WHERE base_info_Id = %s'
        data = (base_info_Id,)
        result = saofudb.select_one_record(query, data)

        self.expected_result['cashLeastCost'] = result[0]
        self.expected_result['cashReduceCost'] = result[1]
        GetInCoupon.cash_reduce_cost = result[1]
        self.expected_result['discount'] = result[2]
        GetInCoupon.discount = result[2]

        logger.info(response['cwc']['cw']['baseInfo']['codeType'])
        # 断言
        self.assertEqual(response['getByWeixin'], bool(self.expected_result['getByWeixin']), msg='getByWexin不为false')
        self.assertEqual(response['cwc']['cw']['baseInfo']['codeType'], self.expected_result['codeType'], msg='codeType不为2')
        self.assertEqual(response['cwc']['cw']['baseInfo']['title'], self.expected_result['title'], msg='title错误')
        self.assertEqual(response['cwc']['cw']['baseInfo']['subTitle'], self.expected_result['subTitle'], msg='subTitle错误')
        self.assertEqual(response['cwc']['cw']['baseInfo']['notice'], self.expected_result['notice'], msg='notice错误')
        self.assertEqual(response['cwc']['cw']['baseInfo']['description'], self.expected_result['description'], msg='description错误')
        self.assertEqual(response['cwc']['cw']['baseInfo']['useLimit'], self.expected_result['useLimit'], msg='useLimit错误')
        self.assertEqual(response['cwc']['cw']['baseInfo']['dateInfoType'], self.expected_result['dateInfoType'], msg='dateInfoType错误')
        self.assertEqual(response['cwc']['cw']['baseInfo']['cardType'], self.expected_result['cardType'], msg='cardType不为1')
        self.assertEqual(response['cwc']['cw']['baseInfo']['listing'], self.expected_result['listing'], msg='listing不为1')
        self.assertEqual(response['cwc']['cw']['baseInfo']['fitAll'], bool(self.expected_result['fitAll']), msg='fitAll不为true')
        self.assertEqual(response['cwc']['cw']['baseInfo']['listing'], self.expected_result['listing'], msg='listing不为1')
        self.assertEqual(response['cwc']['cw']['baseInfo']['detailTxt'], self.expected_result['detailTxt'], msg='detail_txt错误')
        self.assertEqual(response['cwc']['cw']['baseInfo']['servicePhone'], self.expected_result['servicePhone'], msg='servicePhone错误')
        self.assertEqual(response['cwc']['cw']['cashLeastCost'], self.expected_result['cashLeastCost'], msg='cashReduceCost错误')
        self.assertEqual(response['cwc']['cw']['cashReduceCost'], self.expected_result['cashReduceCost'], msg='cashReduceCost错误')
        self.assertEqual(response['cwc']['cw']['discount'], self.expected_result['discount'], msg='discount计算错误')
        self.assertEqual(response['cwc']['channel'], self.expected_result['channel'], msg='channel不为-1')
        self.assertEqual(response['cwc']['branchId'], self.expected_result['branchId'], msg='branchId不为-1')
        self.assertEqual(response['success'], bool(self.expected_result['success']), msg='success不为ture,领取卡券失败')
        self.assertEqual(sku_quantity_new, self.expected_result['skuQuantity'], msg='库存计算错误')

