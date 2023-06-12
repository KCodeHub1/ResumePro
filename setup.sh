mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"xyz@gmail.com\"\n\
" > ~/.streamlit/config.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
\n\
[theme]\n\
base = \"light\"\n\
primaryColor = \"#336699\"\n\
backgroundColor = \"#F6F6F6\"\n\
secondaryBackgroundColor = \"#FFFFFF\"\n\
textColor = \"#333333\"\n\
font = \"sans serif\"\n\
" > ~/.streamlit/config.toml