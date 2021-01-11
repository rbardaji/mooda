# mooda.emso.post_user_email(*message*)

## Reference

Send an email to help@emso-eu.org.

### Parameters

* message: dict
    {'subject': 'Subject of the email',
     'content': 'Content of the email'}

### Returns

* response_message: Response from the API (str)

### Example

```python
import mooda as md

emso = md.util.EMSO(user='LOGIN', password='PASSWORD')


```

Return to [Index](../../index_api_reference.md).
