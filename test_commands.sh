#! /bin/bash

echo 'listing forms...'
abstra list forms

echo 'listing env vars...'
abstra list vars

echo 'listing packages...'
abstra list packages

echo 'listing files...'
abstra list files

echo 'adding env vars...'
abstra add vars ENVIROMENT=production

echo 'removing env vars...'
abstra remove vars ENVIROMENT

echo 'adding packages...'
abstra add packages pandas

echo 'removing packages...'
abstra remove packages pandas

echo 'adding files...'
abstra add files README.md

echo 'removing files...'
abstra remove files README.md

echo 'adding new form...'
form_id=$(abstra add form --name="Form name" --code "x = read('test')" --background '#fffeee' --main-color red --start-message 'start message' --error-message 'error-message' --end-message 'end message' --start-button-text 'start button text' --restart-button-text 'restart button text' --show-sidebar --allow-restart)

form_id=$( echo $form_id | awk -F'Form created successfully: ' '{print $2}')

echo 'updating form...'
abstra update form $form_id --name="Another name" --code "x = read('another test')" --background '#fff555' --main-color blue --start-message 'start message' --error-message 'error-message' --end-message 'end message' --start-button-text 'start button text' --restart-button-text 'restart button text' --show-sidebar --allow-restart

echo 'running form...'
abstra play form $form_id

echo 'removing form...'
abstra remove form $form_id
