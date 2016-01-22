from model import Model

class ModelWeixin(Model):
	__table__ = 'weixin'
	__mapping__ = {
		'id':'weixin_id',
		'weixin_en':'weixinnum_id',
		'name':'name',
		'intro':'intro',
		'link':'link',
		'qrcode':'qrcode',
		'date':'date',
		'head_img':'head_img'
	}