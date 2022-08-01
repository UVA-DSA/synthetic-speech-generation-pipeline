with open("combined_medical_notes.txt", "r") as f:
    text_data = f.readlines()[0]


num_characters = len(text_data)
num_words = len(text_data.split(" "))
print("Number of characters: ", num_characters)
print("Number of words: ", num_words)
print("Approximate speaking time (minutes): ", num_words/150)   #average speaking rate is 150 WPM

length_list = [len(word) for word in text_data.split(" ")]
average_word_length = sum(length_list)/len(length_list)
print("Average word length:", average_word_length)

# 10 minutes worth of audio
def calculate_price(speaking_time):
    num_words = speaking_time * 150
    num_chars = num_words * average_word_length
    return num_chars * 16/1000000


print("Price for 10 min of audio: $", calculate_price(10))
print("Price for 20 min of audio: $", calculate_price(20))
print("Price for 100 min of audio: $", calculate_price(100))
