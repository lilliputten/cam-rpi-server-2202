See:

- [ssmtp to send emails – Raspberry Pi Projects](https://raspberry-projects.com/pi/software_utilities/email/ssmtp-to-send-emails)
- [How to Send SMTP Email using Raspberry Pi](https://iotdesignpro.com/projects/sending-smtp-email-using-raspberry-pi)


Start local debugging smtp server with:
```python
sudo python -m smtpd -c DebuggingServer -n localhost:1025
```

Or use ssmtp:

```
sudo apt-get install ssmtp
sudo apt-get install mailutils
sudo vim /etc/ssmtp/ssmtp.conf
```

Use next params for `ssmtp.conf`:

```
# hostname=raspberrypi
root=postmaster

# mailhub=smtp.gmail.com:587
mailhub=smtp.yandex.ru:465
AuthUser=dmia@yandex.ru
AutPass=PASS
UseSTARTTLS=YES
FromLineOverride=YES
```

Test send mail command (?):

```
echo "hello" | mail s "test subject" lilliputten@yandex.ru
```

See also:

- https://www.instructables.com/Raspberry-Pi-Motion-Detection-Security-Camera/

