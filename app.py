from flask import Flask, request
import requests
import logging
import json
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info(f'Response: {response!r}')
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Привет! Хочешь пройти квиз?'
        sessionStorage[user_id] = {
            'game_started': False,  # здесь информация о том, что пользователь начал игру. По умолчанию False
            'colour': None,
            'attempt': 1,
            'school': None
        }
        # Кнопки подсказки внизу
        res['response']['buttons'] = [
            {
                'title': 'Да',
                'hide': True
            },
            {
                'title': 'Нет',
                'hide': True
            }
        ]
        return
    else:
        if not sessionStorage[user_id]['game_started']:
            if 'да' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['game_started'] = True
                do_response(res, req)
            elif 'нет' in req['request']['nlu']['tokens']:
                res['response']['text'] = 'Ну и ладно!'
                res['response']['end_session'] = True
            else:
                res['response']['text'] = 'Не поняла ответа! Так да или нет?'
                res['response']['buttons'] = [
                    {
                        'title': 'Да',
                        'hide': True
                    },
                    {
                        'title': 'Нет',
                        'hide': True
                    }
                ]
        else:
            if check_answer(req):
                do_response(res, req)
            else:
                res['response']['text'] = 'Не поняла ответа! Попробуйте еще раз.'


def do_response(res, req):
    user_id = req['session']['user_id']
    attempt = sessionStorage[user_id]['attempt']
    if attempt == 1:
        res['response']['text'] = 'В ближайшую субботу у вас есть выбор куда пойти, что вы предпочтёте? ' \
                                  'Пляжную вечеринку, ужин вдвоём, торжественный гала ужин или диджей пати в клубе?'
        res['response']['buttons'] = [
            {
                'title': 'Пляжная вечеринка',
                'hide': True
            },
            {
                'title': 'Ужин вдвоём',
                'hide': True
            },
            {
                'title': 'Торжественный гала ужин',
                'hide': True
            },
            {
                'title': 'Диджей пати в клубе',
                'hide': True
            }
        ]
    elif attempt == 2:
        res['response']['text'] = 'Сколько вам лет?'
    elif attempt == 3:
        res['response']['text'] = 'К просмотру есть 4 фильма, какой вы выберете? ' \
                                  'Грязные танцы с Партиком Суэйзи, Давайте потанцуем с Ричардом Гиром, ' \
                                  'Запах женщины с Аль Пачино или Супер Майкл иксиксэль с Ченингом Татумом.'
        res['response']['buttons'] = [
            {
                'title': 'Грязные танцы',
                'hide': True
            },
            {
                'title': 'Давайте потанцуем',
                'hide': True
            },
            {
                'title': 'Запах женщины',
                'hide': True
            },
            {
                'title': 'Супер Майкл иксиксэль',
                'hide': True
            }
        ]
    elif attempt == 4:
        res['response']['text'] = 'Оцените свой танцевальный уровень по шкале от 1 до 5. 1 - я не умею танцевать, ' \
                                  '5 - я король танцпола.'
        res['response']['buttons'] = [
            {
                'title': '1',
                'hide': True
            },
            {
                'title': '2',
                'hide': True
            },
            {
                'title': '3',
                'hide': True
            },
            {
                'title': '4',
                'hide': True
            },
            {
                'title': '5',
                'hide': True
            }
        ]
    elif attempt == 5:
        res['response']['text'] = 'Какой танец из трёх вы выбрали бы для своего свадебного танца? ' \
                                  'Медленный вальс, аргентинское танго, сальса.'
        res['response']['buttons'] = [
            {
                'title': 'Медленный вальс',
                'hide': True
            },
            {
                'title': 'Аргентинское танго',
                'hide': True
            },
            {
                'title': 'Сальса',
                'hide': True
            }
        ]
    elif attempt == 6:
        res['response']['text'] = 'Какой цвет из представленных, вам больше всего нравится? Фиолетовый, красный, ' \
                                  'синий, оранжевый, зелёный, жёлтый, пудровый, бирюзовый.'
        res['response']['buttons'] = [
            {
                'title': 'Фиолетовый',
                'hide': True
            },
            {
                'title': 'Красный',
                'hide': True
            },
            {
                'title': 'Синий',
                'hide': True
            },
            {
                'title': 'Оранжевый',
                'hide': True
            },
            {
                'title': 'Зелёный',
                'hide': True
            },
            {
                'title': 'Жёлтый',
                'hide': True
            },
            {
                'title': 'Пудровый',
                'hide': True
            },
            {
                'title': 'Бирюзовый',
                'hide': True
            }
        ]
    elif attempt == 7:
        if sessionStorage[user_id]['colour'] == 'Фиолетовый':
            res['response']['text'] = 'Анализирую ваши ответы...'
            res['response']['text'] = 'Вы человек с ярким темпераментом. ' \
                                      'Вы всегда смотрите в будущее и абсолютно не злопамятны, ' \
                                      'хотя память у вас хорошая))) Вы инициативная и энергичная личность и легки на подъем! ' \
                                      'Но вам не интересны долгие и монотонные занятия - движение, вот ваше все! ' \
                                      'Я рекомендую вам остановить свой взгляд на танцах в стиле Caribbean STYLE: ' \
                                      'сальса, бачата, меренге и так же сюда попадает танец КИЗОМБА, это некая смесь танго и бачаты.'
        elif sessionStorage[user_id]['colour'] == 'Красный':
            res['response']['text'] = 'Анализирую ваши ответы...'
            res['response']['text'] = 'Вы ярко выраженная личность. Ваше настроение может измениться в любую минуту. ' \
                                      'Энергичный, инициативный и импульсивный - вот вероятнее всего, ' \
                                      'что думают о вас ваши знакомые. Рядом с вами не бывает скучно, ' \
                                      'да и вы скучать не любите. И не смотря на то, ' \
                                      'что вы ярко переживаете любые события, вы скорее незлопамятны и очень отходчивы. ' \
                                      'С большим энтузиазмом беретесь за новые и интересные дела ' \
                                      'и с успехом доводите их до конца, главное чтобы работа не была долгой и монотонной. ' \
                                      'Как только на горизонте маячит монотонность - это конец любому вашему начинанию. ' \
                                      'Я рекомендую вам остановить свой взгляд на Аргентинском танго.'
        elif sessionStorage[user_id]['colour'] == 'Синий':
            res['response']['text'] = 'Анализирую ваши ответы...'
            res['response']['text'] = 'Вы серьезный человек, возможно немного скрытный. ' \
                                      'Но не смотря на внешнюю сдержанность внутри есть огонь. ' \
                                      'Вы предпочитаете строить планы и раскладывать все по полочкам. ' \
                                      'Красоту любите во всем, что вас окружает. Вам нравятся романтические истории, ' \
                                      'но вы их немного боитесь, так как боитесь быть обиженными. ' \
                                      'И вы очень не любите несправедливость. Я рекомендую вам остановить свой взгляд на ' \
                                      'европейской программе бальных танцев и особое внимание обратить на ВАЛЬС.'
        elif sessionStorage[user_id]['colour'] == 'Оранжевый':
            res['response']['text'] = 'Анализирую ваши ответы...'
            res['response']['text'] = 'Вы яркая и эмоциональная личность. Вашей любви к жизни можно только позавидовать. ' \
                                      'При всей своей внутренней скорости вы в то же время очень уравновешенный человек. ' \
                                      'С большой отдачей беретесь за работу, которая вам интересна. ' \
                                      'Вы неплохо приспосабливаетесь к новому окружению. ' \
                                      'Жизнь для вас это источник новых ощущений. Вам всегда хочется чего то нового. ' \
                                      'Общительный и открытый, вот как скорее всего вас описали бы знакомые. ' \
                                      'Я рекомендую вам остановить свой взгляд на ' \
                                      'европейской программе бальных танцев и особое внимание обратить на танец Квикстеп.'
        elif sessionStorage[user_id]['colour'] == 'Зелёный':
            res['response']['text'] = 'Анализирую ваши ответы...'
            res['response']['text'] = 'Скорее всего вы не стремитесь проявлять свои чувства и эмоции на публике. ' \
                                      'Ваши решения качественные и взвешенные. Спокойный и уравновешенный человек, ' \
                                      'вот как бы вас описали ваши знакомые. В вашем характере есть настойчивость и даже упорство. ' \
                                      'При это вы достаточно дружелюбный человек. Если говорить про танцы, ' \
                                      'то вам может понравиться направление в стиле DANCE FITNESS - ZUMBA.'
        elif sessionStorage[user_id]['colour'] == 'Жёлтый':
            res['response']['text'] = 'Анализирую ваши ответы...'
            res['response']['text'] = 'Вы крайне энергичный и легкий на подъем человек, который очень любит движение. ' \
                                      'Вам присуща быстрота реакции и даже возможно вы любите сопровождать свою речь жестикуляцией. ' \
                                      'Но абсолютно точно нельзя сказать, что вы неуравновешенный человек. ' \
                                      'Каждое дело за которое вы беретесь будет доведено до конца, если вызывает ваш интерес. ' \
                                      'Друзья бы про вас сказали, что вы общительный человек и легко приспосабливаетесь к новому окружению. ' \
                                      'Я рекомендую вам остановить свой взгляд на латиноамериканской программе ' \
                                      'бальных танцев и особое внимание обратить на САМБУ.'
        elif sessionStorage[user_id]['colour'] == 'Пудровый':
            res['response']['text'] = 'Анализирую ваши ответы...'
            res['response']['text'] = 'Вы неспешны и любите размеренный образ жизни. Но это абсолютно не означает, ' \
                                      'что в вас нет огня. Скорее это того, ' \
                                      'что вы не спешите проявлять свои чувства на публику. Прагматичен и ответственен, ' \
                                      'вот как описали бы вас ваши знакомые. А еще вы обладаете достаточным упорством ' \
                                      '(конечно когда вам это лично нужно), чтобы достичь любой поставленной цели. ' \
                                      'Я рекомендую вам остановить свой взгляд на европейской программе бальных танцев и ' \
                                      'особое внимание обратить на ВЕНСКИЙ ВАЛЬС.'
        elif sessionStorage[user_id]['colour'] == 'Бирюзовый':
            res['response']['text'] = 'Анализирую ваши ответы...'
            res['response']['text'] = 'Вы очень нежный и романтичный человек и скорее всего очень ранимый. ' \
                                      'Вы склонны к глубоким переживаниям чувств, ' \
                                      'но при этом всегда верите в светлое будущее. В начатых вами делах, чаще всего, ' \
                                      'проявляете себя как идеальный труженик и стараетесь доводить все до логического конца. ' \
                                      'В большинстве случаев Вы хорошо умеете держать себя в руках. ' \
                                      'Возможно в чем-то вам не всегда хватает решимости. ' \
                                      'Я рекомендую вам остановить свой взгляд на европейской программе бальных танцев и ' \
                                      'особое внимание обратить на ВЕНСКИЙ ВАЛЬС.'
    elif attempt == 8:
        res['response']['text'] = sessionStorage[user_id]['school']


def check_answer(req):
    user_id = req['session']['user_id']
    attempt = sessionStorage[user_id]['attempt']
    if attempt == 1:
        for token in req['request']['nlu']['tokens']:
            if token.lower() in ['вечеринка', 'вечеринку']:
                sessionStorage[user_id]['attempt'] += 1
                return 'Пляжная вечеринка'
            elif token.lower() in ['вдвоём', 'вдвоем']:
                sessionStorage[user_id]['attempt'] += 1
                return 'Ужин вдвоём'
            elif token.lower() in ['торжественный', 'торжественый']:
                sessionStorage[user_id]['attempt'] += 1
                return 'Торжественный гала ужин'
            elif token.lower() == 'диджей':
                sessionStorage[user_id]['attempt'] += 1
                return 'Диджей пати в клубе'
        return None

    if attempt == 2:
        for entity in req['request']['nlu']['entities']:
            if entity['type'] == 'YANDEX.NUMBER':
                sessionStorage[user_id]['attempt'] += 1
                return entity['value']
        return None

    if attempt == 3:
        for token in req['request']['nlu']['tokens']:
            if token.lower() == 'грязные':
                sessionStorage[user_id]['attempt'] += 1
                return 'Грязные танцы'
            elif token.lower() == 'давайте':
                sessionStorage[user_id]['attempt'] += 1
                return 'Давайте потанцуем'
            elif token.lower() == 'запах':
                sessionStorage[user_id]['attempt'] += 1
                return 'Запах женщины'
            elif token.lower() == 'майкл':
                sessionStorage[user_id]['attempt'] += 1
                return 'Супер Майкл иксиксэль'
        return None

    if attempt == 4:
        for entity in req['request']['nlu']['entities']:
            if entity['type'] == 'YANDEX.NUMBER':
                sessionStorage[user_id]['attempt'] += 1
                return entity['value']
        return None

    if attempt == 5:
        for token in req['request']['nlu']['tokens']:
            if token.lower() == 'вальс':
                sessionStorage[user_id]['attempt'] += 1
                return 'Медленный вальс'
            elif token.lower() == 'танго':
                sessionStorage[user_id]['attempt'] += 1
                return 'Аргентинское танго'
            elif token.lower() in ['сальса', 'сальсу']:
                sessionStorage[user_id]['attempt'] += 1
                return 'Сальса'
        return None

    if attempt == 6:
        for token in req['request']['nlu']['tokens']:
            if token.lower() == 'фиолетовый':
                sessionStorage[user_id]['attempt'] += 1
                sessionStorage[user_id]['colour'] = 'Фиолетовый'
                return 'Фиолетовый'
            elif token.lower() == 'красный':
                sessionStorage[user_id]['attempt'] += 1
                sessionStorage[user_id]['colour'] = 'Красный'
                return 'Красный'
            elif token.lower() == 'синий':
                sessionStorage[user_id]['attempt'] += 1
                sessionStorage[user_id]['colour'] = 'Синий'
                return 'Синий'
            elif token.lower() == 'оранжевый':
                sessionStorage[user_id]['attempt'] += 1
                sessionStorage[user_id]['colour'] = 'Оранжевый'
                return 'Оранжевый'
            elif token.lower() in ['зелёный', 'зеленый']:
                sessionStorage[user_id]['attempt'] += 1
                sessionStorage[user_id]['colour'] = 'Зелёный'
                return 'Зелёный'
            elif token.lower() in ['жёлтый', 'желтый']:
                sessionStorage[user_id]['attempt'] += 1
                sessionStorage[user_id]['colour'] = 'Жёлтый'
                return 'Жёлтый'
            elif token.lower() == 'пудровый':
                sessionStorage[user_id]['attempt'] += 1
                sessionStorage[user_id]['colour'] = 'Пудровый'
                return 'Пудровый'
            elif token.lower() == 'бирюзовый':
                sessionStorage[user_id]['attempt'] += 1
                sessionStorage[user_id]['colour'] = 'Бирюзовый'
                return 'Бирюзовый'
        return None
    if attempt == 7:
        address = get_address(req)
        logging.info(address)
        coords = get_coords(address)
        logging.info(coords)
        school = get_school(coords)
        logging.info(coords)
        if school:
            sessionStorage[user_id]['attempt'] += 1
            sessionStorage[user_id]['school'] = school
        return school


def get_address(req):
    adr = ''
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            for key, val in entity['value'].items():
                adr = adr + ',' + val
    if adr:
        return adr
    return None


def get_coords(address):
    try:
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": address,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params).json()
        return response['response']["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['Point']['pos'].split()
    except Exception as e:
        return None


def get_school(coords):
    try:
        search_api_server = 'https://search-maps.yandex.ru/v1/'
        API_KEY = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
        search_param = {
            'apikey': API_KEY,
            'text': 'школа танцев',
            'll': ','.join(coords),
            'lang': 'ru_RU',
        }
        response = requests.get(search_api_server, search_param).json()
        adr = response['features'][0]["properties"]["CompanyMetaData"]["address"]
        return adr
    except Exception as e:
        return None


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
