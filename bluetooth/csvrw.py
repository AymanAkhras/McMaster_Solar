import csv
import time


row = [2,2,3,4,5,6,7,8,9]
start = time.time()
for i in range(1, 100):
    with open('spam.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(row)
        csvfile.close()
        # print(sum(1 for row in csvfile))

end = time.time()
print(f"Runtime of the program is {end - start}")
    # spamwriter.writerow(['Spams'] * 5 + ['Baked Beans'])
# spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])