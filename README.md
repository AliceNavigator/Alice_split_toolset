# Alice_split_toolset
Split audio using the .srt file, clean up annotations, then merge and package into a format suitable for bert-vits2 in a standard manner.   
使用.srt文件分割音频并清洗标注，合并封装至适用于bert-vits2的一个较为标准的格式

**usage 使用
- 将wav和srt文件放入input，依照顺序执行，更多详细参数见-h
```bash
python split.py --mono
python clean_list.py --filter_english
python merge.py
python pack.py baki
```
