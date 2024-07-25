from Dic import topics
import time
import alogrithms
import tracemalloc
from tabulate import tabulate

def load_words(file_path):

    # Remove double quotes from file_path
    file_path = file_path.replace('"', '')

    # import words of atrticle 
    try:
        with open(file_path, 'r') as file:
            words = [word.lower() for word in file.read().split()]
    except FileNotFoundError:
        print("Sorry the file doesn't exist")
    return words


def filter_words(text): #Takes an array of the input form the file and remove from it the common engilsh words
    file = "common-english-words.txt"
    with open(file , "r") as com_words_file: 
        com_w_content = com_words_file.read().split(",") #com_w_content now is an array that contains the common words.

    filtered_words = []

    for word in text:
        if alogrithms.binarySearch(com_w_content,word) == False:
            filtered_words.append(word)

    return filtered_words


def count_words(filtered_words , n):
    word_count = {}
    for word in filtered_words:
        if word in word_count:
            word_count[word] += 1 #Increments the value by 1.
        else:
            word_count[word] = 1
    
    word_count_list = list(word_count.items()) #convert the dict to a list of tuples.
    sorting_algorithms = [alogrithms.smartBubbleSort , alogrithms.selectionSort , alogrithms.mergeSort , alogrithms.quickSort , alogrithms.insertionSort]

    time_taken = []
    memory_used = []

    for x in range(len(sorting_algorithms)):
        word_count_list_copy = word_count_list.copy()

        tracemalloc.start() # Start tracing memroy allocations
        start_time = time.perf_counter()
        sorting_algorithms[x](word_count_list_copy)
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()  # Get memory usage
        tracemalloc.stop()  # Stop tracing memory allocations
        time_taken.append((end_time-start_time) * 1000) # Time in milliseconds
        memory_used.append(peak / 1024**2)  # Convert bytes to megabytes

        for i in range(len(time_taken)):
            time_taken[i] = round(time_taken[i] , 4)

        for i in range(len(memory_used)):
            memory_used[i] = round(memory_used[i] , 4)

    alogrithms.smartBubbleSort(word_count_list)
    top_n_items = word_count_list[-n:]
    return top_n_items , time_taken , memory_used


def classify_text(top):
    topics_dict = { #The key is the string and the value is the instance class
        "health": topics.health(),
        "tech": topics.technology(),
        "travel": topics.travelAndTourism(),
        "science": topics.science(),
        "art": topics.artAndCulture(),
        "politics": topics.politics(),
        "economy": topics.economy(),
    }

    for word, count in top: 
        for topic, instance in topics_dict.items(): 
            if word in instance.words:
                instance.adding_count_to_score(count)


    highest_score = 0
    main_topic = None
    for topic, instance in topics_dict.items():
        if instance.score > highest_score:
            highest_score = instance.score
            main_topic = topic

    if main_topic is not None:
        print(f"The provided article is talking about {main_topic} ")

    else:
        print("Undefined")

def create_table(time, memory):
    data = [
        [" Algorithm Name ", " Time (ms) ", "Memory (MB)"],
        ["Smart bubble sort", time[0], memory[0]],
        ["Selection sort", time[1], memory[1]],
        ["Merge sort", time[2], memory[2]],
        ["Quick sort", time[3], memory[3]],
        ["Insertion sort", time[4], memory[4]]
    ]

    # Specify the table headers
    headers = data[0]

    # Remove the headers from the data
    data = data[1:]

    # Print the formatted table
    table = tabulate(data, headers, tablefmt="fancy_grid" , numalign="right" , stralign="center") # Modify the padding and marging
    print(table)


path = input("Enter a the file path to classify: \n") 
words = load_words(path)
filteredWords = filter_words(words)


top_n_items, time_taken, memory_used = count_words(filteredWords , 10)
classify_text(top_n_items)
create_table(time_taken , memory_used)













