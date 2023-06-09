
function intoDigit(number, digit) {
  return number.toLocaleString('en-US', {
   	minimumIntegerDigits: digit,
    useGrouping: false
  })
}

var inputboxCount = 1; 

function addInputbox() {
	const mainBlock = document.getElementById('searchinput-everything')
	const allSelects = mainBlock.getElementsByTagName('select')
	const allInputs = mainBlock.getElementsByTagName('input')

	const memory = new Object()
	for (var i = allSelects.length - 1; i >= 0; i--) {
		var e = allSelects[i]
		//console.log(e.name + " -> " + e.value)
		memory[e.name] = e.value
	}
	for (var i = allInputs.length - 1; i >= 0; i--) {
		var e = allInputs[i]
		//console.log(e.name + " -> " + e.value)
		memory[e.name] = e.value
	}

	const counter = intoDigit( inputboxCount, 2 )
	mainBlock.innerHTML += `
		<div class="input-group" style="width:80%; margin-left:10%; scale:125%; background-color:gray;">
		  <div class="input-group-addon" style="width:15%; background-color:gray; scale:101%;">
		    <select name="andor-${counter}" style="text-align:center; background-color:gray; color:white;">
          <option value="AND" selected>与</option>
     	  	<option value="OR">或</option>
     	  	<option value="NOT">不包括</option>
  			</select>
		  </div>
		  <div class="input-group-addon" style="width:20%; background-color:gray; padding:0;">
		    <select name="column-${counter}" style="text-align:center; background-color:gray; color:white;">
          <option value="全部字段" selected>全部字段</option>
          <option value="链接">链接</option>
          <option value="标题">标题</option>
          <option value="日期">日期</option>
          <option value="发文机构">发文机构</option>
          <option value="正文">正文</option>
          <option value="索引号">索引号</option>
          <option value="发文字号">发文字号</option>
          <option value="分类">分类</option>
          <option value="地区">地区</option>
    	  </select>
		  </div>
		  <input type="text" class="form-control" name="searchinput-${counter}" style="width:100%; background-color:gray; color:white; ">
		  <div class="input-group-addon btn" style="width:7%; background-color:gray; scale:101%;" onclick="addInputbox()">
		    <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512">
		      <path fill="white" d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32V224H48c-17.7 0-32 14.3-32 32s14.3 32 32 32H192V432c0 17.7 14.3 32 32 32s32-14.3 32-32V288H400c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"/>
		    </svg>
		  </div>
		</div><br>
	`
	for (var i = Object.keys(memory).length - 1; i >= 0; i--) {
		var key = Object.keys(memory)[i]
		var val = memory[key]
		//console.log("key="+key+" -> "+"val="+val)
		document.getElementsByName(key)[0].value = val
	}

	inputboxCount += 1
}

function toggleDoSearch(text) {
	document.getElementById('do-search').value = text
}
