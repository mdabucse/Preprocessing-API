import json
def company(raw_data):
    processed_data = {
        "address_line1": raw_data.get("street"),
        "address_line2": raw_data.get("street2"),
        "city": raw_data.get("city"),
        "company_name": raw_data.get("name"),
        "country": raw_data.get("country_id")[1] if isinstance(raw_data.get("country_id"), list) else raw_data.get("country_id"),
        "country_id": raw_data.get("country_id")[0] if isinstance(raw_data.get("country_id"), list) else raw_data.get("country_id"),
        "crm_id": raw_data.get("id"),
        "display_name": raw_data.get("display_name"),
        "email": raw_data.get("email"),
        "industry": raw_data.get("industry_id"),
        "mobile_number": raw_data.get("mobile"),
        "phone_number": raw_data.get("phone"),
        "postal_code": raw_data.get("zip"),
        "state": raw_data.get("state_id")[1] if isinstance(raw_data.get("state_id"), list) else raw_data.get("state_id"),
        "state_id": raw_data.get("state_id")[0] if isinstance(raw_data.get("state_id"), list) else raw_data.get("state_id"),
        "website_url": raw_data.get("website")
    }
    return processed_data

def individual(raw_data):
    processed_data = {
        "address_line1": raw_data.get("street"),
        "address_line2": raw_data.get("street2"),
        "city": raw_data.get("city"),
        "company": raw_data.get("parent_id")[1] if isinstance(raw_data.get("parent_id"), list) else None,
        "company_id": raw_data.get("parent_id")[0] if isinstance(raw_data.get("parent_id"), list) else None,
        "country": raw_data.get("country_id")[1] if isinstance(raw_data.get("country_id"), list) else None,
        "country_id": raw_data.get("country_id")[0] if isinstance(raw_data.get("country_id"), list) else None,
        "crm_id": raw_data.get("id"),
        "display_name": raw_data.get("display_name"),
        "email": raw_data.get("email"),
        "full_name": raw_data.get("name"),
        "job_title": raw_data.get("function"),
        "mobile_number": raw_data.get("mobile"),
        "phone_number": raw_data.get("phone"),
        "postal_code": raw_data.get("zip"),
        "state": raw_data.get("state_id")[1] if isinstance(raw_data.get("state_id"), list) else None,
        "state_id": raw_data.get("state_id")[0] if isinstance(raw_data.get("state_id"), list) else None
    }
    return processed_data

def interactions(raw_data):
    formatted_data = {
        "author": raw_data.get("author_name") or (raw_data.get("author_id")[1] if isinstance(raw_data.get("author_id"), list) else None),
        "author_id": raw_data.get("author_id")[0] if isinstance(raw_data.get("author_id"), list) else raw_data.get("author_id"),
        "content": raw_data.get("body"),
        "crm_id": raw_data.get("id"),
        "interaction_date": raw_data.get("date"),
        "interaction_type": raw_data.get("message_type"),
        "related_entity_id": raw_data.get("res_id"),
        "related_entity_type": raw_data.get("model"),
        "subject": raw_data.get("subject"),
        "subtype": raw_data.get("subtype_id")[1] if isinstance(raw_data.get("subtype_id"), list) else raw_data.get("message_subtype"),
        "subtype_id": raw_data.get("subtype_id")[0] if isinstance(raw_data.get("subtype_id"), list) else None
    }
    return formatted_data


def lead(raw_data):
    processed_data = {
        "close_date": raw_data.get("date_deadline"),
        "company": raw_data.get("customer_company_name") or (raw_data.get("partner_id")[1] if isinstance(raw_data.get("partner_id"), list) else None),
        "company_id": raw_data.get("customer_company_id") or (raw_data.get("partner_id")[0] if isinstance(raw_data.get("partner_id"), list) else None),
        "contact_name": raw_data.get("contact_name"),
        "created_at": raw_data.get("create_date"),
        "crm_id": raw_data.get("id"),
        "description": raw_data.get("description"),
        "email": raw_data.get("email_from"),
        "expected_value": raw_data.get("expected_revenue"),
        "mobile_number": raw_data.get("mobile"),
        "opportunity_name": raw_data.get("name"),
        "owner": raw_data.get("salesperson_name") or (raw_data.get("user_id")[1] if isinstance(raw_data.get("user_id"), list) else None),
        "owner_id": raw_data.get("user_id")[0] if isinstance(raw_data.get("user_id"), list) else None,
        "phone_number": raw_data.get("phone"),
        "priority": raw_data.get("priority"),
        "probability": raw_data.get("probability"),
        "record_type": raw_data.get("type"),
        "stage": raw_data.get("stage_name") or (raw_data.get("stage_id")[1] if isinstance(raw_data.get("stage_id"), list) else None),
        "stage_id": raw_data.get("stage_id")[0] if isinstance(raw_data.get("stage_id"), list) else None,
        "updated_at": raw_data.get("write_date")
    }
    return processed_data
