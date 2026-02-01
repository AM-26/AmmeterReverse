# AmmeterReverse
保肝护肝的电表倒转小程序，在界园界面刷到令节点就能用啦。因为是在本地给paddleocr准备的annaconda环境运行的，所以直接跑.py文件不大行，pyinstaller打包出来的exe高达4G大小,压缩包放度盘了：AmmeterReverse.rar 链接: https://pan.baidu.com/s/1Dp3ULlIRhHG5xHGM6Jn1tQ?pwd=dae3 提取码: dae3
### 更新了adb路径设置 ~~之前写死了别人用不了~~

游客分队6衡6厉不像9厉1花百分百投钱成功，单纯记录按键位置的话碰到投钱失败就崩，所以加了对投钱失败的处理逻辑，失败时令姐还有概率给第二次机会，更麻烦啦🤪🤪
### 更新了后勤分队的功能，实测不一定非要9厉1花，5厉3花1衡前几次运气好也转起来啦😝😝

唯一的爆炸方式是网卡了，导致时间轴错乱，整体都点不该点的地方，为避免发生此种状况每步操作都等了几秒，在测试容易卡的地方甚至等到10秒，不在运行时突然进行上传下载任务应该就没事，测试时爆炸的三次一次是中途开始上传大文件到网盘，一次是半路开梯子，还有一次单纯家里网炸了

## 必要条件
1. ~~雷电模拟器~~1920*1080分辨率
2. ~~游客分队~~ 现在游客后勤都可以啦😉详见https://www.bilibili.com/opus/1094537681990320135?from=search&spm_id_from=333.337.0.0
3. 开始前模拟器放在这个界面：<img width="1920" height="1080" alt="Screenshot_20250901-173801" src="https://github.com/user-attachments/assets/772150e4-507d-4ff0-80e0-707f97e0b33d" />
## 软件图解（适用于游客分队版本）
⚽设备控制页：
<img width="1989" height="1318" alt="1" src="https://github.com/user-attachments/assets/773ef14c-bd69-43ed-b09a-543328462d4d" />
新版设备控制页，自定义adb路径，填上后手动点一下连接
<img width="1487" height="611" alt="image" src="https://github.com/user-attachments/assets/71434d26-3a6e-4159-9a7b-0461d414f380" />

⚽点击操作页：
<img width="2859" height="882" alt="2" src="https://github.com/user-attachments/assets/626334e0-e589-48e1-a6e7-12c064d213a2" />
⚽获取坐标页：
<img width="1488" height="757" alt="3" src="https://github.com/user-attachments/assets/cf69c089-fe87-43e6-b4de-bcac8b4388db" />
⚽坐标页点加载图片之后：
<img width="1477" height="1011" alt="4 (2)" src="https://github.com/user-attachments/assets/63071e64-f1b4-438d-a4a7-be319f6af7d9" />
## 更新的后勤分队功能：<br>
def logisticsAR(self):<br>
&emsp;        counter = 1<br>
&emsp;        while(1):<br>
            &emsp;&emsp;print(f"第{counter}轮:\n")<br>
            &emsp;&emsp;self.targetOCR()<br>
            &emsp;&emsp;self.logi_getFire_count = int(self.logi_get_fire_entry.get())<br>
            &emsp;&emsp;print(f"获取{self.logi_getFire_count}组烛火（每组6点）\n")<br>
            &emsp;&emsp;self.logi_getTicket_count = int(self.logi_get_ticket_entry.get())<br>
            &emsp;&emsp;print(f"获取{self.logi_getTicket_count}组票卷（每组12张）\n")<br>
            &emsp;&emsp;while(self.dice):<br>
                &emsp;&emsp;&emsp;&emsp;self.logisticsGetMoney()<br>
&emsp;&emsp;            while(self.logi_getFire_count):<br>
            &emsp;&emsp;&emsp;&emsp;    self.logisticsGetFire()<br>
                &emsp;&emsp;&emsp;&emsp;self.logi_getFire_count -= 1<br>
            &emsp;&emsp;while(self.logi_getTicket_count):<br>
                &emsp;&emsp;&emsp;&emsp;self.logisticsGetTicket()<br>
                &emsp;&emsp;&emsp;&emsp;self.logi_getTicket_count -= 1<br>
            &emsp;&emsp;time.sleep(3)<br> 
            &emsp;&emsp;counter += 1<br>
⚽更新的后勤分队内容：
<img width="2866" height="1648" alt="屏幕截图 2025-09-14 124215" src="https://github.com/user-attachments/assets/4cf801b8-30f6-43f8-afbf-d291d0d3a38f" />
⚽后勤分队按钮图解：
<img width="2879" height="1658" alt="屏幕截图 2025-09-14 125724" src="https://github.com/user-attachments/assets/95f6c1c1-e5af-4eda-b270-d95a2f41abea" />
## TIPS:后勤分队也要像游客分队一样先获取令节点坐标哦😋😋


## 添加了AmmeterReverseENV.yml文件，方便直接跑python，省的网盘下载慢啦




