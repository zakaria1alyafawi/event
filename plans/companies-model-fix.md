# Fix RetrieveCompanies.list_paginated

Append to Models/Companies/RetrieveCompanies.py after get_paginated_by_zone return dict:

```
    def list_paginated(self, search=None, event_id=None, zone_id=None, booth_number=None, page=1, limit=20):
        page = max(1, page)
        limit = min(100, max(1, limit))
        query = self.session.query(CompaniesModel).filter(CompaniesModel.deleted_at.is_(None))

        if event_id:
            event_id = validate_uuid(event_id, "event_id")
            query = query.filter(CompaniesModel.event_id == event_id)

        if zone_id:
            zone_id = validate_uuid(zone_id, "zone_id")
            query = query.filter(CompaniesModel.zone_id == zone_id)

        if search:
            query = query.filter(CompaniesModel.name.ilike(f"%{search}%"))

        if booth_number:
            query = query.filter(CompaniesModel.booth_number.ilike(f"%{booth_number}%"))

        total = query.count()

        query = query.options(
            joinedload(CompaniesModel.zone),
            joinedload(CompaniesModel.event)
        ).order_by(CompaniesModel.created_at.desc()).offset((page - 1) * limit).limit(limit)

        companies = query.all()

        company_list = []
        for company in companies:
            zone_name = company.zone.name if company.zone else None
            event_name = company.event.title if company.event else None
            company_dict = {
                "id": str(company.id),
                "name": company.name,
                "booth_number": company.booth_number,
                "slug": company.slug,
                "logo_url": company.logo_url,
                "description": company.description,
                "website": company.website,
                "industry": company.industry,
                "email": company.email,
                "phone": company.phone,
                "zone_id": str(company.zone_id) if company.zone_id else None,
                "zone_name": zone_name,
                "event_id": str(company.event_id),
                "event_name": event_name,
                "created_at": company.created_at.isoformat() if company.created_at else None
            }
            company_list.append(company_dict)

        return {"data": company_list, "total": total, "page": page, "limit": limit}
```

Restart app.