#!/bin/bash
# Script to setup pipenv and install requirements

read -r -p "Do you wish to set pipenv? (Y/n): "
if [[ $REPLY =~ ^[Yy]$ ]] || [[ $REPLY == "" ]]; then
    pip install pipenv
    pipenv --three sync
fi

read -r -p "Do you wish to set API_TOKEN? (Y/n): "
  if [[ $REPLY =~ ^[Yy]$ ]] || [[ $REPLY == "" ]]; then
      sed -i '/export API_TOKEN/d' /home/"$USER"/.bashrc
      read -r -s -p "Enter API_TOKEN: " bot_token
      echo "export API_TOKEN=$bot_token" >> /home/"$USER"/.bashrc
      source "$USER"/.bashrc
      echo "RESTART YOUR TERMINAL"
  fi
