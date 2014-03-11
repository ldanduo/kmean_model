##使用kmeans模型对新闻数据进行聚类
#使用简要说明
python test.py word_dict.txt center_file.txt input_data.txt output_file.txt
word_dict.txt : 新闻词带，即统计语料中的词频率，去掉单字以及只出现一次的词
center_file.txt : 从语料中抽取5篇作为初始的中心点。为了效果明显，每类别中选取一篇作为初始中心。
input_data.txt : 已用空格进行了分词,每一行代表一篇文件。
output_file.txt : 输出文件

#函数说明
* __load_word_dict(dict_file) : 加载词袋
* __get_vsm() : 将新闻转换成词向量
* __distance() : 计算每篇新闻到中心余弦的距离，
                 (x1*y1 +...+ xn*yn)/(sqrt(x1*x1+..+xn*xn)*sqrt(y1*y1+...+yn*yn))
                 每次已经对质心进行了归一化。而在计算一篇新闻到各个质心距离并进行比较时，并不需要考虑，新闻本身模的大小。
* init_center() : 对质心建立倒排，大大提高计算速度。word:list 每行为一个词，每列为该词在质心中的得分即权重。
* __assigment(article_vsm) : 计算每篇文件到质心的距离，并判断文章类别。
* __adjust_center() : 重新计算同一类别即同一簇中的质心。取平均并对质心做归一化
* __center_cmp() : 判断质心改变
* __cluster() : 主函数

#reference
http://zengkui.blog.163.com/blog/static/2123000822012101784440471/
