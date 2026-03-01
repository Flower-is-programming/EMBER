# **EMBER**

I was bored… I hope that says enough.
⚠️ - This project is insecure. There is no rate limiting/ensuring subject is set before the BYE command is ran etc. This is more of a proof of concept. Not a production-ready tool. This *may* change in the future.

---

## **How It Works**

Let’s say:

* The sending server is **SS**
* The receiving server is **RS**

### (Client Connected)

```
RS: 202 Accepted
SS: DOMAIN mail.skylord.linkpc.net
RS: 202 Accepted
SS: FROM username
RS: 202 Accepted
SS: TO otherusername
RS: 202 Accepted
SS: SUBJECT The Subject
RS: 202 Accepted
SS: BODY Hello,\n this is multi-line ;D
RS: 202 Accepted
SS: BYE
```

---

## **FAQ**

### How does EMBER verify that a message is actually from the domain?

```
EMBER verifies that the message is coming from the correct domain by checking the IP address that the domain’s MX record indirectly points to.
```

---

### Does EMBER support TLS?

```
If configured properly — yes. EMBER is more of a hobby project, so TLS support depends on how you set it up.
```

---

### Why should I use EMBER?

```
Because you're cool, right?
```

---
