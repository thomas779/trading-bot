# Introduction
Simple market-making bot designed to narrow spreads and entice volume.

# Improvements
I wrote this in Python as a personal experiment. As I scale this, I
will rewrite this entirely in another programming language.

If development time was not of the essence, I would have:
- Used a performance-based programming language (C++, Rust).
- Ditched http for websockets.
- Server location.
- Improved typecasting on JSON posts and requests.
- Sorting algorithms on my bids and asks.

# Installation Process (PROD)
1. Insall python3 virtual environment module
```bash
apt install python3.10-venv
```
2. create local environment 
```bash
# just on the first time do this
python3 -m venv .venv      # sets up the venv first time

# do this every time before starting the server
source .venv/bin/activate
```
3. Install required packages
```bash 
pip install -r requirements.txt
```
4. Copy `.env` from local environment to production server
```bash
# create dotfile
touch .env

# this is where you add your keys
nano .env

# OPTIONAL: confirmed saved chagnes to .env file
cat .env
```
5. Run the program
```bash
python3 http/probit/main.py
```