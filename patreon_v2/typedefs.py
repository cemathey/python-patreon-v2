import pydantic
from datetime import datetime
import enum


class ChargeStatus(enum.Enum):
    paid = "paid"
    declined = "declined"
    deleted = "deleted"
    pending = "pending"
    refunded = "refunded"
    fraud = "fraud"
    other = "other"


class PledgeType(enum.Enum):
    start = "pledge_start"
    upgrade = "pledge_upgrade"
    downgrade = "pledge_downgrade"
    delete = "pledge_delete"
    subscription = "subscription"


class PatronStatus(enum.Enum):
    active = "active_patron"
    declined = "declined_patron"
    former = "former_patron"
    none = None

    def is_successful(self):
        return self.value == PatronStatus.active


class DeliveryStatus(enum.Enum):
    delivered = "delivered"
    not_delivered = "not_delivered"
    wont_deliver = "wont_deliver"


class Address(pydantic.BaseModel):
    addressee: str | None
    city: str
    country: str
    created_at: datetime
    line_1: str | None
    line_2: str | None
    phone_number: str | None
    postal_code: str | None
    state: str | None

    # relationships
    campaigns: list["Campaign"]
    user: "User"


class Benefit(pydantic.BaseModel):
    app_external_id: str | None
    app_meta: ...  #  | None
    benefit_type: str | None
    created_at: datetime
    deliverables_due_today_count: int
    delivered_deliverables_count: int
    description: str | None
    is_deleted: bool | None
    is_ended: bool
    is_published: bool
    next_deliverable_due_date: datetime | None
    not_delivered_deliverables_count: int
    rule_type: str | None
    tiers_count: int
    title: str

    # relationships
    campaign: "Campaign"
    campaign_installation: ...
    deliverables: list["Deliverable"]
    tiers: list["Tier"]


class Campaign(pydantic.BaseModel):
    created_at: datetime
    creation_name: str | None
    discord_server_id: str | None
    google_analytics_id: str | None
    has_rss: bool
    has_sent_rss_notify: bool
    image_small_url: str
    image_url: str
    is_charged_immediately: bool | None
    is_monthly: bool
    is_nsfw: bool
    main_video_embed: str | None
    main_video_url: str | None
    one_liner: str | None
    patron_count: int
    pay_per_name: str | None
    pledge_url: str
    published_at: datetime | None
    rss_artwork_url: str | None
    rss_feed_title: str
    show_earnings: bool
    summary: str | None
    thanks_embed: str | None
    thanks_msg: str | None
    thanks_video_url: str | None
    url: str
    vanity: str | None


class Deliverable(pydantic.BaseModel):
    completed_at: datetime
    delivery_status: DeliveryStatus
    due_at: datetime

    # relationships
    benefit: "Benefit"
    campaign: "Campaign"
    member: "Member"
    user: "User"


class Goal(pydantic.BaseModel):
    amount_cents: int
    completed_percentage: int
    created_at: datetime
    description: str | None
    reached_at: datetime | None
    title: str

    # relationships
    campaign: "Campaign"


class Media(pydantic.BaseModel):
    created_at: datetime
    download_url: str
    file_name: str
    image_urls: ...
    metadata: ...
    mimetype: str
    owner_id: str
    owner_relationship: str
    owner_type: str
    size_bytes: int
    state: str
    upload_expires_at: datetime
    upload_parameters: ...
    upload_url: str


class Member(pydantic.BaseModel):
    campaign_lifetime_support_cents: int
    currently_entitled_amount_cents: int
    lifetime_support_cents: int
    will_pay_amount_cents: int
    email: str
    full_name: str
    is_follower: str
    last_charge_date: datetime | None
    last_charge_status: ChargeStatus
    next_charge_date: datetime | None
    note: str
    patron_status: PatronStatus
    pledge_cadence: int
    pledge_relationship_start: datetime | None

    # relationships
    address: Address
    campaign: Campaign
    currently_entitled_tiers: list["Tier"]
    pledge_history: list["PledgeEvent"]
    user: "User"


class OAuthClient(pydantic.BaseModel):
    author_name: str | None
    client_secret: str
    description: str
    domain: str | None
    icon_url: str | None
    name: str
    privacy_policy_url: str | None
    redirect_uris: str
    tos_url: str | None
    version: int


class PledgeEvent(pydantic.BaseModel):
    amount_cents: int
    currency_code: str
    date: datetime
    payment_status: ChargeStatus
    tier_id: str
    tier_title: str
    type: PledgeType

    # relationships
    campaign: Campaign
    patron: "User"
    tier: "Tier"


class Post(pydantic.BaseModel):
    app_id: int | None
    app_status: str | None
    content: str | None
    embed_data: ...  #  | None
    embed_url: str | None
    is_paid: bool | None
    is_public: bool | None
    tiers: list["Tier"] | None
    published_at: datetime | None
    title: str | None
    url: str


class Tier(pydantic.BaseModel):
    amount_cents: int
    created_at: datetime
    description: str
    discord_role_ids: ...  #  | None
    edited_at: datetime
    image_url: str | None
    patron_count: int
    post_count: int | None
    published: bool
    published_at: datetime | None
    remaining: int | None
    requires_shipping: bool
    title: str
    unpublished_at: datetime | None
    url: str
    user_limit: int | None

    # relationships
    benefits: list[Benefit]
    campaign: Campaign
    tier_image: Media


class User(pydantic.BaseModel):
    about: str | None
    can_see_nsfw: bool | None
    created: datetime
    email: str
    first_name: str | None
    last_name: str | None
    full_name: str
    hide_pledges: bool | None
    image_url: str
    is_email_verified: bool
    like_count: int
    social_connections: ...
    thumb_url: str
    url: str
    vanity: str | None

    # relationships
    campaign: Campaign
    memberships: list[Member]


class Webhook(pydantic.BaseModel):
    last_attempted_at: datetime
    num_consecutive_times_failed: int
    paused: bool
    secret: str
    triggers: ...
    uri: str
