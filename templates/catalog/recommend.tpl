{% include 'catalog/header.tpl' %}
<div class="container recommend-page">
	<h1>
		推荐公众号
	</h1>
	<p id="hint" class="mt20"></p>
	<div class="recommend" id="recommend">
		<input type="text" name="weixin" placeholder="公众号名称"/>
		<input type="text" name="weixinnum_id" placeholder="公众号ID"/>
		<button class="btn" onclick="submit(this)">确定</button>
	</div>
</div>
<script type="text/javascript" src="/static/js/zjhlib-1.0.js"></script>
<script type="text/javascript">
	function submit(othis){
		var ele = z.get('recommend'),
			weixin = z.nth(ele,0).value || '',
			weixinnum_id = z.nth(ele,1).value || '',
			hint = z.get('hint');

		if(weixin.length < 5){
			z.html(hint,'公众号名称太短');
			return;
		}
		if(weixinnum_id.length < 5){
			z.html(hint,'公众号ID太短');
			return;
		}
		othis.disabled = true;
		z.POST('/recommend',{'weixin':weixin,'weixinnum_id':weixinnum_id},function(r){
			r = r.trim();
			if(r == 'success'){
				z.html(hint,'推荐成功，谢谢！');
				z.nth(ele,0).value = null;
				z.nth(ele,1).value = null;
			}else{
				z.html(hint,r);
			}
			othis.disabled = false;
		});
	}
</script>
{% include 'catalog/footer.tpl' %}