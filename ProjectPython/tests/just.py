

def main():
    for x in [1, 2, 3, 4 ,5 ]:
      yield x


if __name__ == "__main__":
    number=main()
    print(next(number))
    print(next(number))
    print(next(number))
    print(next(number))





