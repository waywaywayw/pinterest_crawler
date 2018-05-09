# pinterest_crawler

1. 先在制定的目录下创建一个空文件：board名_page_source.html <br>
  比如我设置的目录是 Rootpath = os.path.join('E:\\', '站点图片下载', 'pinterest', 'percylee1817')<br>
  需要的board是 https://www.pinterest.com/percylee1817/machine/<br>
  那么在percylee1817文件夹下 创建空文件： machine_page_source.html<br>
 
2. 先登录pinterest账号，然后进入https://www.pinterest.com/percylee1817/machine/<br>
    然后一直滑到底..（可以录个按键精灵来滑..）<br>
   （Chrome为例）按F12打开 开发者工具，找到Elements栏。<br>
    找到<html 那一行，右键 -> copy -> copy element<br>
    打开第1步的空文件，复制进去，保存。<br>
    
3. 在项目的givenURL.txt里添加一行：https://www.pinterest.com/percylee1817/machine/<br>
  运行就好 = =
  
总结来说，就是先把缓存文件保存到本地，然后程序解析下载图片 = =
