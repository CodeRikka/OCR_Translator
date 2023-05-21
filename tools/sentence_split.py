from nltk.tokenize import sent_tokenize

def sentence_token_nltk(str):
    sent_tokenize_list = sent_tokenize(str)
    return sent_tokenize_list

if __name__ == "__main__":
    sent = "fact that there are two sides in every investment transaction: \"The one with the greatest information is likely to come out ahead: It takes a and scudy huge amount of work and investigation. Templeton claimed that diligence had played a much greater role in his success than innate talent: He often spoke of his determination to ( O give the extra ounce tO make the extra call, to schedule the extra meeting;"
    for i in sentence_token_nltk(sent):
        print(i)