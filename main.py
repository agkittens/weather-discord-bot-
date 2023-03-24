import discord
import requests
import random
import giphy_client

# tokens/keys should have their own unique sequence
DISCORD_TOKEN = None
API_KEY = None
API_KEY_GIPHY = None

intents = discord.Intents.all()
client = discord.Client(intents=intents)
apiInstance = giphy_client.DefaultApi()

@client.event
async def on_ready():
    print('✧･ﾟ: *✧･ﾟ♡*(ᵘʷᵘ)*♡･ﾟ✧*:･ﾟ✧\n' f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    if message.content.startswith('!weather '):
        city = message.content[9:]
        weatherURL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
        response = requests.get(weatherURL)
        weatherData = response.json()

        if weatherData["cod"] == '404':
            embed = discord.Embed(title = '✧･ﾟ: *✧･ Weather ･ﾟ✧*:･ﾟ✧', color =0xfafafa, description=f'City {city} has not been found')
            await message.channel.send(embed=embed)

        #WEATHER INIT
        elif weatherData["cod"] == 200:
            kelvin = 273
            country = weatherData['sys']['country']
            temp = int(weatherData['main']['temp']) - kelvin
            pressure = weatherData['main']['pressure']
            humidity = weatherData['main']['humidity']
            windSpeed = int(weatherData['wind']['speed'] * 3.6)
            overcast = weatherData['clouds']['all']
            sky = weatherData['weather'][0]['description']

        #CITY RANDOM GIF
            apiResponse = apiInstance.gifs_search_get(API_KEY_GIPHY, city, limit=10, rating='g')
            gif = random.choice(list(apiResponse.data))

        #EMBED MESSAGE
            embed = discord.Embed(title=f"✧･ﾟ: *✧･ﾟ Weather of {city} in {country} ･ﾟ✧*:･ﾟ✧", color=0xfafafa)
            embed.add_field(name="temperature", value=temp, inline=True)
            embed.add_field(name="pressure", value=pressure, inline=True)
            embed.add_field(name="humidity", value=humidity, inline=True)
            embed.add_field(name="wind speed", value=windSpeed, inline=True)
            embed.add_field(name="overcast %", value=overcast, inline=True)
            embed.add_field(name="sky status", value=sky, inline=True)
            embed.set_thumbnail(url=gif.images.downsized.url)
            await message.channel.send(embed=embed)

client.run(DISCORD_TOKEN)
