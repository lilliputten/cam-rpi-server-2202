Start local debugging smtp server with:
```python
sudo python -m smtpd -c DebuggingServer -n localhost:1025
```

Or use ssmtp:

```
sudo apt-get install ssmtp
sudo vim /etc/ssmtp/ssmtp.conf
```

Use next params for `ssmtp.conf`:

```
mailhub=smtp.yandex.ru:465
AuthUser=dmia@yandex.ru
AutPass=Xtre225yM
UseSTARTTLS=YES
```

Test send mail command (?):

```
echo "hello" | mail s "test" dmia@yandex.ru
```

See also:

- https://www.instructables.com/Raspberry-Pi-Motion-Detection-Security-Camera/

