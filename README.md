# AmmeterReverse
保肝护肝的电表倒转小程序，在界园界面刷到令节点就能用啦。因为是在本地给paddleocr准备的annaconda环境运行的，所以直接跑.py文件不大行，pyinstaller打包出来的exe高达4G大小,压缩包放度盘了： https://pan.baidu.com/s/17kWIi-PmRtDaa1tJiFlLWQ?pwd=2jve 提取码: 2jve

游客分队6衡6厉不像9厉1花百分百投钱成功，单纯记录按键位置的话碰到投钱失败就崩，所以加了对投钱失败的处理逻辑，失败时令姐还有概率给第二次机会，更麻烦啦🤪🤪

唯一的爆炸方式是网卡了，导致时间轴错乱，整体都点不该点的地方，为避免发生此种状况每步操作都等了几秒，在测试容易卡的地方甚至等到10秒，不在运行时突然进行上传下载任务应该就没事，测试时爆炸的三次一次是中途开始上传大文件到网盘，一次是半路开梯子，还有一次单纯家里网炸了

## 必要条件
1. 雷电模拟器，1920*1080分辨率
2. 游客分队，详见https://www.bilibili.com/opus/1094537681990320135?from=search&spm_id_from=333.337.0.0
3. 开始前模拟器放在这个界面：<img width="1920" height="1080" alt="Screenshot_20250901-173801" src="https://github.com/user-attachments/assets/772150e4-507d-4ff0-80e0-707f97e0b33d" />
## 软件图解
⚽设备控制页：
<img width="1989" height="1318" alt="1" src="https://github.com/user-attachments/assets/b344ee58-94c8-4294-bc16-e39c0ab21c66" />
⚽点击操作页：
<img width="2859" height="882" alt="2" src="https://github.com/user-attachments/assets/626334e0-e589-48e1-a6e7-12c064d213a2" />
⚽获取坐标页：
<img width="1488" height="757" alt="3" src="https://github.com/user-attachments/assets/cf69c089-fe87-43e6-b4de-bcac8b4388db" />
⚽坐标页点加载图片之后：
<img width="1477" height="1011" alt="4 (2)" src="https://github.com/user-attachments/assets/63071e64-f1b4-438d-a4a7-be319f6af7d9" />

## annaconda环境的包（paddleocr的环境，所以一堆包）
- packages in environment at D:\paddleOCR:

- Name                    Version                   Build  Channel
- aiohappyeyeballs          2.6.1                    pypi_0    pypi
- aiohttp                   3.12.15                  pypi_0    pypi
- aiosignal                 1.4.0                    pypi_0    pypi
- altgraph                  0.17.4                   pypi_0    pypi
- annotated-types           0.7.0                    pypi_0    pypi
- anyio                     4.9.0                    pypi_0    pypi
- aom                       3.6.0                hd77b12b_0
- attrs                     25.3.0                   pypi_0    pypi
- beautifulsoup4            4.13.4                   pypi_0    pypi
- bzip2                     1.0.8                h2bbff1b_6
- ca-certificates           2025.7.15            haa95532_0
- cabarchive                0.2.4              pyhd8ed1ab_1    conda-forge
- cachetools                6.1.0                    pypi_0    pypi
- cairo                     1.16.0               h85cdd14_6
- certifi                   2025.6.15                pypi_0    pypi
- chardet                   5.2.0                    pypi_0    pypi
- charset-normalizer        3.4.2                    pypi_0    pypi
- colorama                  0.4.6                    pypi_0    pypi
- colorlog                  6.9.0                    pypi_0    pypi
- cssselect                 1.3.0                    pypi_0    pypi
- cssutils                  2.11.1                   pypi_0    pypi
- cuda-cccl_win-64          12.9.27                       0    nvidia
- cuda-command-line-tools   12.9.1                        0    nvidia
- cuda-compiler             12.9.1                        0    nvidia
- cuda-crt-dev_win-64       12.9.86                       0    nvidia
- cuda-crt-tools            12.9.86                       0    nvidia
- cuda-cudart               12.9.79                       0    nvidia
- cuda-cudart-dev           12.9.79                       0    nvidia
- cuda-cudart-dev_win-64    12.9.79                       0    nvidia
- cuda-cudart-static        12.9.79                       0    nvidia
- cuda-cudart-static_win-64 12.9.79                       0    nvidia
- cuda-cudart_win-64        12.9.79                       0    nvidia
- cuda-cuobjdump            12.9.82                       1    nvidia
- cuda-cupti                12.9.79                       0    nvidia
- cuda-cupti-dev            12.9.79                       0    nvidia
- cuda-cuxxfilt             12.9.82                       1    nvidia
- cuda-libraries            12.9.1                        0    nvidia
- cuda-libraries-dev        12.9.1                        0    nvidia
- cuda-nvcc                 12.9.86                       0    nvidia
- cuda-nvcc-dev_win-64      12.9.86                       0    nvidia
- cuda-nvcc-impl            12.9.86                       0    nvidia
- cuda-nvcc-tools           12.9.86                       0    nvidia
- cuda-nvcc_win-64          12.9.86                       0    nvidia
- cuda-nvdisasm             12.9.88                       1    nvidia
- cuda-nvml-dev             12.9.79                       1    nvidia
- cuda-nvprof               12.9.79                       0    nvidia
- cuda-nvprune              12.9.82                       1    nvidia
- cuda-nvrtc                12.9.86                       0    nvidia
- cuda-nvrtc-dev            12.9.86                       0    nvidia
- cuda-nvvm-dev_win-64      12.9.86                       0    nvidia
- cuda-nvvm-impl            12.9.86                       0    nvidia
- cuda-nvvm-tools           12.9.86                       0    nvidia
- cuda-nvvp                 12.9.79                       1    nvidia
- cuda-opencl               12.9.19                       0    nvidia
- cuda-opencl-dev           12.9.19                       0    nvidia
- cuda-profiler-api         12.9.79                       0    nvidia
- cuda-sanitizer-api        12.9.79                       1    nvidia
- cuda-toolkit              12.9.1                        0    nvidia
- cuda-tools                12.9.1                        0    nvidia
- cuda-version              12.9                          3    nvidia
- cuda-visual-tools         12.9.1                        0    nvidia
- cx-logging                3.2.1                    pypi_0    pypi
- cx_freeze                 8.4.0           py313h5ea7bf4_1    conda-forge
- dataclasses-json          0.6.7                    pypi_0    pypi
- dav1d                     1.2.1                h2bbff1b_0
- decorator                 5.2.1                    pypi_0    pypi
- distro                    1.9.0                    pypi_0    pypi
- einops                    0.8.1                    pypi_0    pypi
- et-xmlfile                2.0.0                    pypi_0    pypi
- expat                     2.7.1                h8ddb27b_0
- filelock                  3.18.0                   pypi_0    pypi
- fontconfig                2.14.1               hb33846d_3
- freeglut                  3.4.0                h8a1e904_1
- freetype                  2.13.3               h0620614_0
- fribidi                   1.0.10               h62dcd97_0
- frozenlist                1.7.0                    pypi_0    pypi
- fsspec                    2025.7.0                 pypi_0    pypi
- ftfy                      6.3.1                    pypi_0    pypi
- gputil                    1.4.0                    pypi_0    pypi
- graphite2                 1.3.14               hd77b12b_1
- greenlet                  3.2.3                    pypi_0    pypi
- h11                       0.16.0                   pypi_0    pypi
- harfbuzz                  10.2.0               he2f9f60_1
- httpcore                  1.0.9                    pypi_0    pypi
- httpx                     0.28.1                   pypi_0    pypi
- httpx-sse                 0.4.1                    pypi_0    pypi
- huggingface-hub           0.34.3                   pypi_0    pypi
- icu                       73.1                 h6c2663c_0
- idna                      3.10                     pypi_0    pypi
- imagesize                 1.4.1                    pypi_0    pypi
- jinja2                    3.1.6                    pypi_0    pypi
- jiter                     0.10.0                   pypi_0    pypi
- joblib                    1.5.1                    pypi_0    pypi
- jpeg                      9e                   h827c3e9_3
- jsonpatch                 1.33                     pypi_0    pypi
- jsonpointer               3.0.0                    pypi_0    pypi
- khronos-opencl-icd-loader 2024.05.08           h8cc25b3_0
- langchain                 0.3.27                   pypi_0    pypi
- langchain-community       0.3.27                   pypi_0    pypi
- langchain-core            0.3.72                   pypi_0    pypi
- langchain-openai          0.3.28                   pypi_0    pypi
- langchain-text-splitters  0.3.9                    pypi_0    pypi
- langsmith                 0.4.8                    pypi_0    pypi
- lcms2                     2.16                 h62be587_1
- lerc                      4.0.0                h5da7b33_0
- libavif                   1.1.1                h827c3e9_0
- libcublas                 12.9.1.4                      0    nvidia
- libcublas-dev             12.9.1.4                      0    nvidia
- libcufft                  11.4.1.4                      0    nvidia
- libcufft-dev              11.4.1.4                      0    nvidia
- libcurand                 10.3.10.19                    0    nvidia
- libcurand-dev             10.3.10.19                    0    nvidia
- libcusolver               11.7.5.82                     0    nvidia
- libcusolver-dev           11.7.5.82                     0    nvidia
- libcusparse               12.5.10.65                    0    nvidia
- libcusparse-dev           12.5.10.65                    0    nvidia
- libdeflate                1.22                 h5bf469e_0
- libffi                    3.4.4                hd77b12b_1
- libglib                   2.84.2               h405b238_0
- libiconv                  1.16                 h2bbff1b_3
- liblief                   0.16.4               h585ebfc_0
- libmpdec                  4.0.0                h827c3e9_0
- libnpp                    12.4.1.87                     0    nvidia
- libnpp-dev                12.4.1.87                     0    nvidia
- libnvfatbin               12.9.82                       0    nvidia
- libnvfatbin-dev           12.9.82                       0    nvidia
- libnvjitlink              12.9.86                       0    nvidia
- libnvjitlink-dev          12.9.86                       0    nvidia
- libnvjpeg                 12.4.0.76                     0    nvidia
- libnvjpeg-dev             12.4.0.76                     0    nvidia
- libpng                    1.6.39               h8cc25b3_0
- libtiff                   4.7.0                h404307b_0
- libwebp-base              1.3.2                h3d04722_1
- libxml2                   2.13.8               h866ff63_0
- lief                      0.16.6                   pypi_0    pypi
- lxml                      6.0.0                    pypi_0    pypi
- lz4-c                     1.9.4                h2bbff1b_1
- markupsafe                3.0.2                    pypi_0    pypi
- marshmallow               3.26.1                   pypi_0    pypi
- mbedtls                   3.5.1                h5da7b33_1
- more-itertools            10.7.0                   pypi_0    pypi
- multidict                 6.6.3                    pypi_0    pypi
- mypy-extensions           1.1.0                    pypi_0    pypi
- networkx                  3.5                      pypi_0    pypi
- nsight-compute            2025.2.1.3                    0    nvidia
- numpy                     2.2.6                    pypi_0    pypi
- nvidia-cublas-cu12        12.6.4.1                 pypi_0    pypi
- nvidia-cuda-runtime-cu12  12.6.77                  pypi_0    pypi
- nvidia-cudnn-cu12         9.5.1.17                 pypi_0    pypi
- nvidia-cufft-cu12         11.3.0.4                 pypi_0    pypi
- nvidia-curand-cu12        10.3.7.77                pypi_0    pypi
- nvidia-cusolver-cu12      11.7.1.2                 pypi_0    pypi
- nvidia-cusparse-cu12      12.5.4.2                 pypi_0    pypi
- nvidia-nvjitlink-cu12     12.9.86                  pypi_0    pypi
- openai                    1.98.0                   pypi_0    pypi
- opencv-contrib-python     4.10.0.84                pypi_0    pypi
- openjpeg                  2.5.2                h9b5d1b5_1
- openpyxl                  3.1.5                    pypi_0    pypi
- openssl                   3.0.17               h35632f6_0
- opt-einsum                3.3.0                    pypi_0    pypi
- orjson                    3.11.1                   pypi_0    pypi
- packaging                 25.0            py313haa95532_0
- paddleocr                 3.1.0                    pypi_0    pypi
- paddlepaddle-gpu          3.1.0                    pypi_0    pypi
- paddlex                   3.1.3                    pypi_0    pypi
- pandas                    2.3.1                    pypi_0    pypi
- pcre2                     10.42                h0ff8eda_1
- pefile                    2023.2.7                 pypi_0    pypi
- pillow                    11.2.1                   pypi_0    pypi
- pip                       25.1               pyhc872135_2
- pixman                    0.40.0               h2bbff1b_1
- premailer                 3.10.0                   pypi_0    pypi
- prettytable               3.16.0                   pypi_0    pypi
- propcache                 0.3.2                    pypi_0    pypi
- protobuf                  6.31.1                   pypi_0    pypi
- py-cpuinfo                9.0.0                    pypi_0    pypi
- py-lief                   0.16.4          py313h585ebfc_0
- pyclipper                 1.3.0.post6              pypi_0    pypi
- pydantic                  2.11.7                   pypi_0    pypi
- pydantic-core             2.33.2                   pypi_0    pypi
- pydantic-settings         2.10.1                   pypi_0    pypi
- pyinstaller               6.15.0                   pypi_0    pypi
- pyinstaller-hooks-contrib 2025.8                   pypi_0    pypi
- pypdfium2                 4.30.0                   pypi_0    pypi
- pyperclip                 1.9.0                    pypi_0    pypi
- python                    3.13.5          h286a616_100_cp313    anaconda
- python-dateutil           2.9.0.post0              pypi_0    pypi
- python-dotenv             1.1.1                    pypi_0    pypi
- python_abi                3.13                    0_cp313
- pytz                      2025.2                   pypi_0    pypi
- pywin32-ctypes            0.2.3                    pypi_0    pypi
- pyyaml                    6.0.2                    pypi_0    pypi
- regex                     2025.7.34                pypi_0    pypi
- requests                  2.32.4                   pypi_0    pypi
- requests-toolbelt         1.0.0                    pypi_0    pypi
- ruamel-yaml               0.18.14                  pypi_0    pypi
- ruamel-yaml-clib          0.2.12                   pypi_0    pypi
- scikit-learn              1.7.1                    pypi_0    pypi
- scipy                     1.16.1                   pypi_0    pypi
- setuptools                78.1.1          py313haa95532_0
- shapely                   2.1.1                    pypi_0    pypi
- six                       1.17.0                   pypi_0    pypi
- sniffio                   1.3.1                    pypi_0    pypi
- soupsieve                 2.7                      pypi_0    pypi
- sqlalchemy                2.0.42                   pypi_0    pypi
- sqlite                    3.50.2               hda9a48d_1
- striprtf                  0.0.29             pyhd8ed1ab_0    conda-forge
- tenacity                  9.1.2                    pypi_0    pypi
- threadpoolctl             3.6.0                    pypi_0    pypi
- tiktoken                  0.9.0                    pypi_0    pypi
- tk                        8.6.14               h5e9d12e_1
- tokenizers                0.21.4                   pypi_0    pypi
- tqdm                      4.67.1                   pypi_0    pypi
- typing-extensions         4.14.0                   pypi_0    pypi
- typing-inspect            0.9.0                    pypi_0    pypi
- typing-inspection         0.4.1                    pypi_0    pypi
- tzdata                    2025.2                   pypi_0    pypi
- ucrt                      10.0.22621.0         haa95532_0
- ujson                     5.10.0                   pypi_0    pypi
- urllib3                   2.5.0                    pypi_0    pypi
- vc                        14.42                haa95532_5
- vc14_runtime              14.44.35208         h4927774_10
- vs2015_runtime            14.44.35208         ha6b5a95_10
- vs2017_win-64             19.16.27032.1        hb4161e2_3
- vswhere                   2.8.4                haa95532_0
- wcwidth                   0.2.13                   pypi_0    pypi
- wheel                     0.45.1          py313haa95532_0
- xz                        5.6.4                h4754444_1
- yarl                      1.20.1                   pypi_0    pypi
- zlib                      1.2.13               h8cc25b3_1
- zstandard                 0.23.0                   pypi_0    pypi
- zstd                      1.5.6                h8880b57_0




