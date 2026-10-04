"""Synthetic exact-payload chronology check. Evidence authentication remains external."""
from datetime import datetime
from hashlib import sha256

def aware(s):
 t=datetime.fromisoformat(s.replace('Z','+00:00'))
 if t.tzinfo is None or t.utcoffset() is None:raise ValueError('Timezone-aware evidence bounds required')
 return t

def check(archived_payload,current_payload,*,media_capture_upper,event_lower,media_response_authenticated=False,original_media_verified=False,explicit_event_capture_attribution=False,media_role='unknown'):
 if not all([media_response_authenticated,original_media_verified,explicit_event_capture_attribution]):raise ValueError('Missing original-response, payload or attribution evidence')
 if media_role!='capture_of_this_event':raise ValueError('Illustration/background/portrait/unknown use is not this predicate')
 if not isinstance(archived_payload,bytes) or not isinstance(current_payload,bytes) or not archived_payload or not current_payload:raise ValueError('Original nonempty payload bytes required')
 capture=aware(media_capture_upper);event=aware(event_lower)
 same=sha256(archived_payload).digest()==sha256(current_payload).digest()
 return dict(exact_payload_equal=same,strictly_pre_event=capture<event,attribution_review_flag=same and capture<event,whole_incident_disproved=False,evidence_authentication_performed_by_helper=False)
