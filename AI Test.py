from Game import Word, GameManager

if __name__ == "__main__":
    GameManager.read_words()

    triesCount = []
    efficiency = []

    for word in GameManager.words:
        Word.word = word[0]
        Word.form_mask()

        tries = 0

        while not GameManager.endOfGame:
            letter = GameManager.ai_letterSelect()
            GameManager.ai_checkLetter(letter)

            tries += 1

            GameManager.check_isEnd()

        triesCount.append(tries)
        efficiency.append(len(Word.word)/tries)

        GameManager.start_new()

    averTries = 0
    averEff = 0

    for tries, eff in zip(triesCount, efficiency):
        averTries += tries
        averEff += eff

    averTries /= len(triesCount)
    averEff /= len(efficiency)

    for word, tries, eff in zip(GameManager.words, triesCount, efficiency):
        print('Слово \"{0}\". Попыток: {1}. КПД: {2}'.format(word[0], tries, eff))

    print("\nСреднее число попыток: {0}. Средний КПД: {1}".format(averTries, averEff))