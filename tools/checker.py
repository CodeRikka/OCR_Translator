import enchant

def correct_spelling(text):
    # 创建一个英语字典对象
    dictionary = enchant.Dict("en_US")

    corrected_text = []
    words = text.split()
    for word in words:
        # 检查单词是否在字典中存在
        if dictionary.check(word):
            corrected_text.append(word)
        else:
            # 获取可能的正确拼写建议
            suggestions = dictionary.suggest(word)
            if suggestions:
                corrected_word = suggestions[0]  # 获取第一个建议的拼写
                corrected_text.append(corrected_word)
            else:
                corrected_text.append(word)  # 如果没有建议的拼写，则保留原单词

    return ' '.join(corrected_text)

if __name__ == "__main__":
    input_text = "I havv a pen. It is ink."
    corrected_text = correct_spelling(input_text)
    print(corrected_text)
