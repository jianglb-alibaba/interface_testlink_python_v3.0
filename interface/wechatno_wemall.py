#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laiyu'

import urllib.request
import json

from globalpkg.log import logger
from globalpkg.global_var import cookie
from globalpkg.global_var import global_serial
from globalpkg.global_var import global_openId
from globalpkg.global_var import saofudb
from unittesttestcase import MyUnittestTestCase
from htmlparser import  MyHTMLParser
from interface.wecharno_card_coupon import GetInCoupon

__all__ = ['PList', 'Goods', 'AddToCart', 'DelFromCart', 'CartList', 'ToBuyGoods', 'CMOrder', 'Pay5', 'CardPay']
# 打开微商城
class PList(MyUnittestTestCase):
    step_output = None

    def test_plist_default(self):
        content_type = {'Content-Type':'application/x-www-form-urlencoded','charset':'utf-8'}
        headers = content_type.copy()
        #cookie = {'Cookie':'10549840601068216320=ous64uFCCLMyXYDJ-MkNilyCI5C'}
        headers.update(cookie)
        self.http.set_header(headers)

        logger.info('正在发起POST请求...')
        self.params['serial'] = global_serial
        self.params = urllib.parse.urlencode(self.params)  # 将参数转为url编码字符串# 注意，此处params为字典类型的数据
        self.params = self.params.encode('utf-8')
        response = self.http.post(self.url, self.params)
        PList.step_output = response  # 保存返回结果供其它接口使用
        response = response[0].decode('utf-8')
        response = json.loads(response)

        logger.info('正在解析返回结果:%s' % response)

        # 断言
        query = 'SELECT COUNT(*) FROM mall_goods AS mg ' \
                'JOIN mall_goods_cate AS mgc ON mg.cate_id=mgc.id ' \
                'JOIN template_cate AS tc ON tc.cate_id=mgc.id AND tc.template_id=1 AND tc.status=1 ' \
                'WHERE mg.shop_id=%s AND mg.del_flag=%s AND mg.status=%s AND mg.business_id NOT IN (%s, %s)'
        data = (42, 0, 1, 1, 2)
        result = saofudb.select_one_record(query, data)
        totalRows = result[0]
        totalPages = totalRows // int(self.expected_result['pageSize']) + 1

        self.assertEqual(response['pageInfo']['currentPage'], self.expected_result['currentPage'], msg='currentPage不等于1')
        self.assertEqual(response['pageInfo']['pageSize'], self.expected_result['pageSize'], msg='pageSize不等于10')
        self.assertEqual(response['pageInfo']['pageStartRow'], self.expected_result['pageStartRow'], msg='pageStartRow不等于0')
        self.assertEqual(response['pageInfo']['pagination'], bool(self.expected_result['pagination']), msg='pagination不为True')
        self.assertEqual(response['pageInfo']['totalPages'], totalPages, msg='totalPages错误')
        self.assertEqual(response['pageInfo']['totalRows'], totalRows, msg='totalRows错误')

        query = 'SELECT sku_quantity FROM mall_goods WHERE id=%s'
        data = (26838,)
        result = saofudb.select_one_record(query, data)
        skuQuantity1 = result[0]

        query = 'SELECT sku_quantity FROM mall_goods WHERE id=%s'
        data = (26839,)
        result = saofudb.select_one_record(query, data)
        skuQuantity2 = result[0]

        for item in response['dataList']:
            if item['id'] == 26838:
                self.assertEqual(item['name'], self.expected_result['goodsinfo'][0]['name'], msg='商品名称读取错误')
                self.assertEqual(item['price'], self.expected_result['goodsinfo'][0]['price'], msg='商品价格price读取错误')
                self.assertEqual(item['description'], self.expected_result['goodsinfo'][0]['description'], msg='商品描述读取错误')
                self.assertEqual(item['iconUrl'], self.expected_result['goodsinfo'][0]['iconUrl'], msg='商品连接iconUrl读取错误')
                self.assertEqual(item['standard'],  self.expected_result['goodsinfo'][0]['standard'], msg='商品规格读取错误')
                self.assertEqual(item['skuQuantity'], skuQuantity1, msg='商品库存读取错误')
            elif item['id'] == 26839:
                self.assertEqual(item['name'], self.expected_result['goodsinfo'][1]['name'], msg='商品名称读取错误')
                self.assertEqual(item['price'], self.expected_result['goodsinfo'][1]['price'], msg='商品价格price读取错误')
                self.assertEqual(item['description'], self.expected_result['goodsinfo'][1]['description'], msg='商品描述读取错误')
                self.assertEqual(item['iconUrl'], self.expected_result['goodsinfo'][1]['iconUrl'], msg='商品连接iconUrl读取错误')
                self.assertEqual(item['standard'],  self.expected_result['goodsinfo'][1]['standard'], msg='商品规格读取错误')
                self.assertEqual(item['skuQuantity'], skuQuantity2, msg='商品库存读取错误')

# 点击商品
class Goods(MyUnittestTestCase):
    def test_click_goods(self):
        headers = cookie
        self.http.set_header(headers)

        mall_goods_id = self.params['id']

        logger.info('正在发起GET请求...')
        self.params['serial'] = global_serial
        self.params = urllib.parse.urlencode(self.params)  # 将参数转为url编码字符串# 注意，此处params为字典类型的数据
        response = self.http.get(self.url, self.params)
        status_code = response[2]
       # logger.info('正在解析返回结果:%s' % response[0].decode('utf-8'))

        # 解析HTML文档
        parser = MyHTMLParser(strict = False)
        parser.feed(response[0].decode('utf-8'))
        starttag_data = parser.get_starttag_data()

        query = 'SELECT name FROM mall_goods WHERE id=%s'
        data = (mall_goods_id,)
        mall_goods_name = saofudb.select_one_record(query, data)
        mall_goods_name = mall_goods_name[0]
        self.expected_result['goods_name'] = mall_goods_name

        goods_name = ''
        for data in starttag_data:
            if data[1].find(mall_goods_name) != -1:
                goods_name = data[1].replace('\r', '')
                goods_name =goods_name.replace('\n', '')
                goods_name =goods_name.replace('\t', '')

        # 断言
        self.assertEqual(status_code, self.expected_result['status'], msg='http状态码status不等于200')
        self.assertEqual(goods_name, self.expected_result['goods_name'], msg='无法打开商品详情')

# 把商品加入购物车
class AddToCart(MyUnittestTestCase):
    def setUp(self):
        # 初始化购物车数据
        query = 'SELECT id FROM customer WHERE channel_serial=%s'
        data = (global_openId,)
        customer_id = saofudb.select_one_record(query, data)
        customer_id = customer_id[0]

        query = 'UPDATE mall_shopping_cart SET amount = 0 WHERE customer_id = %s and closed=1' % customer_id
        saofudb.execute_update(query)

    strid = None # 供把商品移出购物车使用
    def test_add_to_cart(self):
        headers = cookie
        self.http.set_header(headers)

        self.params['serial'] = global_serial
        self.params['openId'] = global_openId
        self.expected_result['amount'] = self.params['amount']
        self.expected_result['mall_goods_id'] = self.params['mallGoodsId']

        # 提取customer_id供断言使用
        query = 'SELECT id FROM customer WHERE channel_serial=%s'
        data = (self.params['openId'],)
        customer_id = saofudb.select_one_record(query, data)
        customer_id = customer_id[0]

        # 提取shop_id供断言使用
        query = 'SELECT id FROM shop WHERE serial=%s'
        data = (global_serial,)
        shop_id = saofudb.select_one_record(query, data)
        self.expected_result['shop_id'] = shop_id[0]

        logger.info('正在发起POST请求...')
        self.params = urllib.parse.urlencode(self.params)  # 将参数转为url编码字符串# 注意，此处params为字典类型的数据
        self.params = self.params.encode('utf-8')
        response = self.http.post(self.url, self.params)
        response = response[0].decode('utf-8')
        response = json.loads(response)

        logger.info('正在解析返回结果:%s' % response)

        # 断言
        self.assertEqual(response['success'], bool(self.expected_result['success']), '假入购物车失败，success不为True')

        query = 'SELECT amount, mall_goods_id, shop_id, closed, id FROM mall_shopping_cart WHERE customer_id = %s and closed=%s ' \
                'ORDER BY id DESC LIMIT 1'
        data = (customer_id,1)
        result = saofudb.select_one_record(query, data)

        self.assertEqual(result[0], self.expected_result['amount'], msg='购物车商品数amount存储错误')
        self.assertEqual(result[1], self.expected_result['mall_goods_id'], msg='购物车商品mall_goods_id存储错误')
        self.assertEqual(result[2], self.expected_result['shop_id'], msg='购物车商户shop_id存储错误')
        self.assertEqual(result[3], self.expected_result['closed'], msg='购物车closed存储错误')

        AddToCart.strid = result[4]

# 把商品移出购物车
class DelFromCart(MyUnittestTestCase):
    def test_del_from_cart(self):
        headers = cookie
        self.http.set_header(headers)

        self.params['strIds'] = AddToCart.strid
        self.params['serial'] = global_serial

        logger.info('正在发起POST请求...')
        self.params = urllib.parse.urlencode(self.params)  # 将参数转为url编码字符串# 注意，此处params为字典类型的数据
        self.params = self.params.encode('utf-8')
        response = self.http.post(self.url, self.params)
        response = response[0].decode('utf-8')
        response = json.loads(response)

        logger.info('正在解析返回结果:%s' % response)
        query = 'SELECT amount, mall_goods_id, shop_id, closed, id FROM mall_shopping_cart WHERE id=%s'
        data = (AddToCart.strid,)
        result = saofudb.select_one_record(query, data)
        # 断言
        self.assertEqual(response['success'], bool(self.expected_result['success']), '商品移出购物车失败，success不为True')
        self.assertEqual(result, None, msg ='实际未删除购物车记录')

# 查看购物车列表
class CartList(MyUnittestTestCase):
    def test_view_cart_list(self):
        headers = cookie
        self.http.set_header(headers)

        self.params['serial'] = global_serial
        self.params['openId'] = global_openId

        logger.info('正在发起GET请求...')
        self.params = urllib.parse.urlencode(self.params)  # 将参数转为url编码字符串# 注意，此处params为字典类型的数据
        response = self.http.get(self.url, self.params)
        response = response[0].decode('utf-8')
        response = json.loads(response)

        logger.info('正在解析返回结果:%s' % response)

        # 断言
        self.assertEqual(response[0]['amount'], self.expected_result['amount'], msg='购物车中商品总数错误')
        self.assertEqual(response[0]['mallGoods']['id'], self.expected_result['goodsID'], msg='购物车商品缺失')

# 点击立即购买按钮
class ToBuyGoods(MyUnittestTestCase):
    def test_to_buy_goods(self):
        headers = cookie
        self.http.set_header(headers)

        self.params['serial'] = global_serial

        logger.info('正在发起GET请求...')
        self.params = urllib.parse.urlencode(self.params)  # 将参数转为url编码字符串# 注意，此处params为字典类型的数据
        response = self.http.get(self.url, self.params)
        status_code = response[2]
        response_body = response[0].decode('utf-8')

        logger.info('正在解析返回结果:%s' % response_body)

        # 解析HTML文档
        parser = MyHTMLParser(strict = False)
        parser.feed(response_body)
        starttag_data = parser.get_starttag_data()

        tab_page_title = ''
        for data in starttag_data:
            if data[1] == self.expected_result['tab_page_title']:
                tab_page_title = data[1]
                break

        # 断言
        self.assertEqual(status_code, self.expected_result['status'], msg='http状态码status不等于200')
        self.assertEqual(tab_page_title, self.expected_result['tab_page_title'], msg='无法打开商品详情')

# 创建储值卡支付订单
class CMOrder(MyUnittestTestCase):
    attach = ''
    mall_goods_id = ''
    amount = ''

    def test_create_mall_order(self):
        headers = cookie
        self.http.set_header(headers)

        self.params['serial'] = global_serial
        self.params['openId'] = global_openId

        CMOrder.mall_goods_id = self.params['mallGoodsId']
        CMOrder.amount = self.params['amount']

        logger.info('正在发起POST请求...')
        self.params = urllib.parse.urlencode(self.params)  # 将参数转为url编码字符串# 注意，此处params为字典类型的数据
        self.params = self.params.encode('utf-8')
        response = self.http.post(self.url, self.params)
        response = response[0].decode('utf-8')
        response = json.loads(response)

        logger.info(response)

        CMOrder.attach = response['attach'] # 供储值卡支付使用

        # 断言
        self.assertEqual(response['success'], bool(self.expected_result['success']), '创建储值卡支付订单失败，success不为True')

# 提交储值卡支付订单(重定向)
class Pay5(MyUnittestTestCase):
    def test_pay5(self):
        headers = cookie
        self.http.set_header(headers)

        self.params['orderId'] = CMOrder.attach
        self.params['serial'] = global_serial

        logger.info('正在发起GET请求...')
        self.params = urllib.parse.urlencode(self.params)  # 将参数转为url编码字符串# 注意，此处params为字典类型的数据
        response = self.http.get(self.url, self.params)
        response_headers = response[1]
        response_body = response[0].decode('utf-8')
       # logger.info(response_body)

       # 解析HTML文档
        parser = MyHTMLParser(strict = False)
        parser.feed(response_body)
        starttag_data = parser.get_starttag_data()

        page_title = ''
        button_name = ''
        for data in starttag_data:
            if data[1] == self.expected_result['page_title']:
                page_title = data[1]
            if data[1] == self.expected_result['button_name']:
                button_name = data[1]
                break

        # 断言
        self.assertEqual(page_title, self.expected_result['page_title'], msg='打开页面不是储值卡支付界面')
        self.assertEqual(button_name, self.expected_result['button_name'], msg='无法打开确认支付页面')

# 储值卡支付
class CardPay(MyUnittestTestCase):
    def setUp(self):
        # 获取客户id和姓名，shopId
        query = 'SELECT id FROM customer WHERE channel_serial=%s'
        self.params['openId'] = global_openId
        data = (self.params['openId'],)
        result = saofudb.select_one_record(query, data)
        customer_id = result[0]

        # 查询会员账户余额，积分等相关信息
        query = 'SELECT balance, bonus, sum_amount_expend, sum_bonus_expend, balance_total FROM customer_account WHERE customer_id = %s'
        data = (customer_id,)
        result = saofudb.select_one_record(query, data)
        bonus = result[1]    # 会员积分
        #if bonus >


    # 使用会员账户支付，不使用任何优惠，消费无积分赠送
    def test_account_pay_without_discount(self):
        headers = cookie
        self.http.set_header(headers)

        self.params['productOrderId'] = CMOrder.attach
        self.params['openId'] = global_openId

        # 获取商品订单id
        query = 'SELECT id FROM trade_order WHERE product_order_id=%s'
        data = (self.params['productOrderId'],)
        result = saofudb.select_one_record(query, data)
        self.params['orderId'] = result[0]
        order_id = result[0]

        # 获取客户id和姓名，shopId
        query = 'SELECT id, name, shop_id FROM customer WHERE channel_serial=%s'
        data = (self.params['openId'],)
        result = saofudb.select_one_record(query, data)
        self.params['customerId'] = result[0]
        customer_id = result[0]
        self.params['customerName'] = result[1]
        self.params['shopId'] = result[2]
        shop_id = result[2]

        # 查询会员账户余额，积分等相关信息
        query = 'SELECT balance, bonus, sum_amount_expend, sum_bonus_expend, balance_total FROM customer_account WHERE customer_id = %s'
        data = (customer_id,)
        result = saofudb.select_one_record(query, data)
        balance_old = result[0]  # 会员账户余额，单位：分
        bonus_old = result[1]    # 会员积分
        sum_amount_expend_old= result[2]   # 总花费金额，单位：分
        sum_bonus_expend_old = result[3]   # 总花费积分

        logger.info('正在发起POST请求...')
        self.params = urllib.parse.urlencode(self.params)  # 将参数转为url编码字符串# 注意，此处params为字典类型的数据
        self.params = self.params.encode('utf-8')
        response = self.http.post(self.url, self.params)
        response = response[0].decode('utf-8')
        response = json.loads(response)

        logger.info('正在解析返回结果:%s' % response)

        # 查询会员账户余额，积分等相关信息
        query = 'SELECT balance, bonus, sum_amount_expend, sum_bonus_expend, balance_total FROM customer_account WHERE customer_id = %s'
        data = (customer_id,)
        result = saofudb.select_one_record(query, data)
        balance_new = result[0]  # 会员账户余额，单位：分
        bonus_new = result[1]    # 会员积分
        sum_amount_expend_new= result[2]   # 总花费金额，单位：分
        sum_bonus_expend_new = result[3]    # 总花费积分

        # 查询实付金额
        query = 'SELECT receipt_fee FROM trade_order WHERE id = %s'
        data = (order_id,)
        result = saofudb.select_one_record(query, data)
        receipt_fee_new = result[0]

        query = 'SELECT price FROM mall_goods WHERE id = %s'
        data = (CMOrder.mall_goods_id,)
        result = saofudb.select_one_record(query, data)
        goods_price = result[0]

        # 查询运费
        query = 'SELECT deliver_fee FROM mall_config WHERE shop_id = %s'
        data = (shop_id,)
        result = saofudb.select_one_record(query, data)
        deliver_fee = result[0]

        self.expected_result['receipt_fee'] = CMOrder.amount * goods_price + deliver_fee
        self.expected_result['balance'] = balance_old - self.expected_result['receipt_fee']
        self.expected_result['bonus'] = bonus_old
        self.expected_result['sum_amount_expend'] = sum_amount_expend_old + self.expected_result['receipt_fee']
        self.expected_result['sum_bonus_expend'] = sum_bonus_expend_old

        # 断言
        self.assertEqual(response['success'], bool(self.expected_result['success']), '储值卡支付失败（使用会员账户支付，不使用任何优惠）')
        self.assertEqual(receipt_fee_new, self.expected_result['receipt_fee'], msg='消费者实付金额计算错误')
        self.assertEqual(balance_new, self.expected_result['balance'], msg ='消费者余额计算错误')
        self.assertEqual(bonus_new, self.expected_result['bonus'], msg='消费者积分计算错误')
        self.assertEqual(sum_amount_expend_new, self.expected_result['sum_amount_expend'], msg='消费者总花费金额计算错误')
        self.assertEqual(sum_bonus_expend_new, self.expected_result['sum_bonus_expend'], msg='消费者总花费积分计算错误')

    # 会员账户支付，仅使用代金券优惠，消费无积分赠送
    def test_account_pay_with_cash_discount(self):
        headers = cookie
        self.http.set_header(headers)


        self.params['productOrderId'] = CMOrder.attach
        self.params['openId'] = global_openId

        # 获取商品订单id
        query = 'SELECT id FROM trade_order WHERE product_order_id=%s'
        data = (self.params['productOrderId'],)
        result = saofudb.select_one_record(query, data)
        self.params['orderId'] = result[0]
        order_id = result[0]

        # 获取客户id和姓名，shopId
        query = 'SELECT id, name, shop_id FROM customer WHERE channel_serial=%s'
        data = (self.params['openId'],)
        result = saofudb.select_one_record(query, data)
        self.params['customerId'] = result[0]
        customer_id = result[0]
        self.params['customerName'] = result[1]
        self.params['shopId'] = result[2]
        shop_id = result[2]

        # 查询会员账户余额，积分等相关信息
        query = 'SELECT balance, bonus, sum_amount_expend, sum_bonus_expend, balance_total FROM customer_account WHERE customer_id = %s'
        data = (customer_id,)
        result = saofudb.select_one_record(query, data)
        balance_old = result[0]  # 会员账户余额，单位：分
        bonus_old = result[1]    # 会员积分
        sum_amount_expend_old= result[2]   # 总花费金额，单位：分
        sum_bonus_expend_old = result[3]   # 总花费积分

        self.params['yhCardId'] = GetInCoupon.card_code

        logger.info('正在发起POST请求...')
        self.params = urllib.parse.urlencode(self.params)  # 将参数转为url编码字符串# 注意，此处params为字典类型的数据
        self.params = self.params.encode('utf-8')

        response = self.http.post(self.url, self.params)
        response = response[0].decode('utf-8')
        response = json.loads(response)

        logger.info('正在解析返回结果:%s' % response)

        # 查询会员账户余额，积分等相关信息
        query = 'SELECT balance, bonus, sum_amount_expend, sum_bonus_expend, balance_total FROM customer_account WHERE customer_id = %s'
        data = (customer_id,)
        result = saofudb.select_one_record(query, data)
        balance_new = result[0]  # 会员账户余额，单位：分
        bonus_new = result[1]    # 会员积分
        sum_amount_expend_new= result[2]   # 总花费金额，单位：分
        sum_bonus_expend_new = result[3]    # 总花费积分

        # 查询实付金额
        query = 'SELECT receipt_fee FROM trade_order WHERE id = %s'
        data = (order_id,)
        result = saofudb.select_one_record(query, data)
        receipt_fee_new = result[0]

        query = 'SELECT price FROM mall_goods WHERE id = %s'
        data = (CMOrder.mall_goods_id,)
        result = saofudb.select_one_record(query, data)
        goods_price = result[0]

        # 查询运费
        query = 'SELECT deliver_fee FROM mall_config WHERE shop_id = %s'
        data = (shop_id,)
        result = saofudb.select_one_record(query, data)
        deliver_fee = result[0]

        self.expected_result['receipt_fee'] = CMOrder.amount * goods_price - GetInCoupon.cash_reduce_cost + deliver_fee
        self.expected_result['balance'] = balance_old - self.expected_result['receipt_fee']
        self.expected_result['bonus'] = bonus_old
        self.expected_result['sum_amount_expend'] = sum_amount_expend_old + self.expected_result['receipt_fee']
        self.expected_result['sum_bonus_expend'] = sum_bonus_expend_old

        query = 'SELECT id FROM coupon_weixin_customer WHERE serial = %s'
        data = (GetInCoupon.card_code,)
        result = saofudb.select_one_record(query, data)
        id = result[0]

        query = 'SELECT count(*) FROM coupon_weixin_verification WHERE cc_id = %s'
        data = (id,)
        result = saofudb.select_one_record(query, data)
        record_num = result[0]

        # 断言
        self.assertEqual(response['success'], bool(self.expected_result['success']), '储值卡支付失败（使用会员账户支付，不使用任何优惠）')
        self.assertEqual(receipt_fee_new, self.expected_result['receipt_fee'], msg='消费者实付金额计算错误')
        self.assertEqual(balance_new, self.expected_result['balance'], msg ='消费者余额计算错误')
        self.assertEqual(bonus_new, self.expected_result['bonus'], msg='消费者积分计算错误')
        self.assertEqual(sum_amount_expend_new, self.expected_result['sum_amount_expend'], msg='消费者总花费金额计算错误')
        self.assertEqual(sum_bonus_expend_new, self.expected_result['sum_bonus_expend'], msg='消费者总花费积分计算错误')
        self.assertEqual(record_num, self.expected_result['coupon_weixin_verification_record'], msg='代金券核销不成功')

    # 会员账户支付，仅使用折扣券优惠，消费无积分赠送
    def test_account_pay_with_coupon_discount(self):
        headers = cookie
        self.http.set_header(headers)

        self.params['productOrderId'] = CMOrder.attach
        self.params['openId'] = global_openId

        # 获取商品订单id
        query = 'SELECT id FROM trade_order WHERE product_order_id=%s'
        data = (self.params['productOrderId'],)
        result = saofudb.select_one_record(query, data)
        self.params['orderId'] = result[0]
        order_id = result[0]

        # 获取客户id和姓名，shopId
        query = 'SELECT id, name, shop_id FROM customer WHERE channel_serial=%s'
        data = (self.params['openId'],)
        result = saofudb.select_one_record(query, data)
        self.params['customerId'] = result[0]
        customer_id = result[0]
        self.params['customerName'] = result[1]
        self.params['shopId'] = result[2]
        shop_id = result[2]

        # 查询会员账户余额，积分等相关信息
        query = 'SELECT balance, bonus, sum_amount_expend, sum_bonus_expend, balance_total FROM customer_account WHERE customer_id = %s'
        data = (customer_id,)
        result = saofudb.select_one_record(query, data)
        balance_old = result[0]  # 会员账户余额，单位：分
        bonus_old = result[1]    # 会员积分
        sum_amount_expend_old= result[2]   # 总花费金额，单位：分
        sum_bonus_expend_old = result[3]   # 总花费积分

        self.params['yhCardId'] = GetInCoupon.card_code

        logger.info('正在发起POST请求...')
        self.params = urllib.parse.urlencode(self.params)  # 将参数转为url编码字符串# 注意，此处params为字典类型的数据
        self.params = self.params.encode('utf-8')

        response = self.http.post(self.url, self.params)
        response = response[0].decode('utf-8')
        response = json.loads(response)

        logger.info('正在解析返回结果:%s' % response)

        # 查询会员账户余额，积分等相关信息
        query = 'SELECT balance, bonus, sum_amount_expend, sum_bonus_expend, balance_total FROM customer_account WHERE customer_id = %s'
        data = (customer_id,)
        result = saofudb.select_one_record(query, data)
        balance_new = result[0]  # 会员账户余额，单位：分
        bonus_new = result[1]    # 会员积分
        sum_amount_expend_new= result[2]   # 总花费金额，单位：分
        sum_bonus_expend_new = result[3]    # 总花费积分

        # 查询实付金额
        query = 'SELECT receipt_fee FROM trade_order WHERE id = %s'
        data = (order_id,)
        result = saofudb.select_one_record(query, data)
        receipt_fee_new = result[0]

        query = 'SELECT price FROM mall_goods WHERE id = %s'
        data = (CMOrder.mall_goods_id,)
        result = saofudb.select_one_record(query, data)
        goods_price = result[0]

        # 查询运费
        query = 'SELECT deliver_fee FROM mall_config WHERE shop_id = %s'
        data = (shop_id,)
        result = saofudb.select_one_record(query, data)
        deliver_fee = result[0]

        self.expected_result['receipt_fee'] = CMOrder.amount * goods_price * (100 - GetInCoupon.discount) / 10.0 + deliver_fee
        self.expected_result['balance'] = balance_old - self.expected_result['receipt_fee']
        self.expected_result['bonus'] = bonus_old
        self.expected_result['sum_amount_expend'] = sum_amount_expend_old + self.expected_result['receipt_fee']
        self.expected_result['sum_bonus_expend'] = sum_bonus_expend_old

        query = 'SELECT id FROM coupon_weixin_customer WHERE serial = %s'
        data = (GetInCoupon.card_code,)
        result = saofudb.select_one_record(query, data)
        id = result[0]

        query = 'SELECT id FROM coupon_weixin_customer WHERE serial = %s'
        data = (GetInCoupon.card_code,)
        result = saofudb.select_one_record(query, data)
        id = result[0]

        query = 'SELECT count(*) FROM coupon_weixin_verification WHERE cc_id = %s'
        data = (id,)
        result = saofudb.select_one_record(query, data)
        record_num = result[0]

        # 断言
        self.assertEqual(response['success'], bool(self.expected_result['success']), '储值卡支付失败（使用会员账户支付，不使用任何优惠）')
        self.assertEqual(receipt_fee_new, self.expected_result['receipt_fee'], msg='消费者实付金额计算错误')
        self.assertEqual(balance_new, self.expected_result['balance'], msg ='消费者余额计算错误')
        self.assertEqual(bonus_new, self.expected_result['bonus'], msg='消费者积分计算错误')
        self.assertEqual(sum_amount_expend_new, self.expected_result['sum_amount_expend'], msg='消费者总花费金额计算错误')
        self.assertEqual(sum_bonus_expend_new, self.expected_result['sum_bonus_expend'], msg='消费者总花费积分计算错误')
        self.assertEqual(record_num, self.expected_result['coupon_weixin_verification_record'], msg='折扣券核销不成功')


    # 会员账户支付，仅使用积分抵现，消费无积分赠送
    def test_account_pay_with_point_discount(self):
        headers = cookie
        self.http.set_header(headers)

        self.params['productOrderId'] = CMOrder.attach
        self.params['openId'] = global_openId

        # 获取商品订单id
        query = 'SELECT id FROM trade_order WHERE product_order_id=%s'
        data = (self.params['productOrderId'],)
        result = saofudb.select_one_record(query, data)
        self.params['orderId'] = result[0]
        order_id = result[0]

        # 获取客户id和姓名，shopId
        query = 'SELECT id, name, shop_id FROM customer WHERE channel_serial=%s'
        data = (self.params['openId'],)
        result = saofudb.select_one_record(query, data)
        self.params['customerId'] = result[0]
        customer_id = result[0]
        self.params['customerName'] = result[1]
        self.params['shopId'] = result[2]
        shop_id = result[2]

        # 查询会员账户余额，积分等相关信息
        query = 'SELECT balance, bonus, sum_amount_expend, sum_bonus_expend, balance_total FROM customer_account WHERE customer_id = %s'
        data = (customer_id,)
        result = saofudb.select_one_record(query, data)
        balance_old = result[0]  # 会员账户余额，单位：分
        bonus_old = result[1]    # 会员积分
        sum_amount_expend_old= result[2]   # 总花费金额，单位：分
        sum_bonus_expend_old = result[3]   # 总花费积分

        logger.info('正在发起POST请求...')
        self.params = urllib.parse.urlencode(self.params)  # 将参数转为url编码字符串# 注意，此处params为字典类型的数据
        self.params = self.params.encode('utf-8')

        response = self.http.post(self.url, self.params)
        response = response[0].decode('utf-8')
        response = json.loads(response)

        logger.info('正在解析返回结果:%s' % response)

        # 查询会员账户余额，积分等相关信息
        query = 'SELECT balance, bonus, sum_amount_expend, sum_bonus_expend, balance_total FROM customer_account WHERE customer_id = %s'
        data = (customer_id,)
        result = saofudb.select_one_record(query, data)
        balance_new = result[0]  # 会员账户余额，单位：分
        bonus_new = result[1]    # 会员积分
        sum_amount_expend_new= result[2]   # 总花费金额，单位：分
        sum_bonus_expend_new = result[3]    # 总花费积分

        # 查询实付金额
        query = 'SELECT receipt_fee FROM trade_order WHERE id = %s'
        data = (order_id,)
        result = saofudb.select_one_record(query, data)
        receipt_fee_new = result[0]

        query = 'SELECT price FROM mall_goods WHERE id = %s'
        data = (CMOrder.mall_goods_id,)
        result = saofudb.select_one_record(query, data)
        goods_price = result[0]

        # 查询运费
        query = 'SELECT deliver_fee FROM mall_config WHERE shop_id = %s'
        data = (shop_id,)
        result = saofudb.select_one_record(query, data)
        deliver_fee = result[0]

        self.expected_result['receipt_fee'] = CMOrder.amount * goods_price * (100 - GetInCoupon.discount) / 10.0 + deliver_fee
        self.expected_result['balance'] = balance_old - self.expected_result['receipt_fee']
        self.expected_result['bonus'] = bonus_old
        self.expected_result['sum_amount_expend'] = sum_amount_expend_old + self.expected_result['receipt_fee']
        self.expected_result['sum_bonus_expend'] = sum_bonus_expend_old



        # 断言
        self.assertEqual(response['success'], bool(self.expected_result['success']), '储值卡支付失败（使用会员账户支付，不使用任何优惠）')
        self.assertEqual(receipt_fee_new, self.expected_result['receipt_fee'], msg='消费者实付金额计算错误')
        self.assertEqual(balance_new, self.expected_result['balance'], msg ='消费者余额计算错误')
        self.assertEqual(bonus_new, self.expected_result['bonus'], msg='消费者积分计算错误')
        self.assertEqual(sum_amount_expend_new, self.expected_result['sum_amount_expend'], msg='消费者总花费金额计算错误')
        self.assertEqual(sum_bonus_expend_new, self.expected_result['sum_bonus_expend'], msg='消费者总花费积分计算错误')
        self.assertEqual(record_num, self.expected_result['coupon_weixin_verification_record'], msg='折扣券核销不成功')