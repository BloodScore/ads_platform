from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required

from app.auth.models import User
from app.platform import platform_bp
from app.platform.models import Ad, Category
from app.platform.forms import AdCreationForm, SearchForm, PaymentForm


@platform_bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.update(last_seen=datetime.utcnow())


@platform_bp.route('/', methods=['GET', 'POST'])
@platform_bp.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    ads = Ad.query.paginate(page, current_app.config['ADS_PER_PAGE'], False)
    next_url = url_for('platform.index', page=ads.next_num) if ads.has_next else None
    prev_url = url_for('platform.index', page=ads.prev_num) if ads.has_prev else None
    return render_template(
        'platform/index.html',
        ads=sorted(ads.items, key=lambda ad: ad.is_paid, reverse=True),
        next_url=next_url,
        prev_url=prev_url
    )


@platform_bp.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    ads = Ad.query.filter_by(user_id=current_user.id).paginate(page, current_app.config['ADS_PER_PAGE'], False)
    next_url = url_for('platform.index', page=ads.next_num) if ads.has_next else None
    prev_url = url_for('platform.index', page=ads.prev_num) if ads.has_prev else None
    return render_template(
        'platform/profile.html',
        user=user,
        ads=sorted(ads.items, key=lambda ad: ad.is_paid, reverse=True),
        next_url=next_url,
        prev_url=prev_url
    )


@platform_bp.route('/deactivate_account', methods=['GET', 'POST'])
@login_required
def deactivate_account():   # todo Delete related ads
    current_user.update(is_active=False)
    flash('Your account has been deactivated.')
    return redirect(url_for('auth.logout'))


@platform_bp.route('/create_ad', methods=['GET', 'POST'])
@login_required
def create_ad():
    form = AdCreationForm()
    form.categories.choices = [(category.name, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        ad = Ad.create(
            text_description=form.text_description.data,
            location=form.location.data,
            price=form.price.data,
        )
        for category in form.categories.data:
            category_obj = Category.query.filter_by(name=category).first()
            ad.categories.append(category_obj)
        ad.user_id = current_user.id
        ad.user_phone_number = current_user.phone_number
        ad.save()
        flash('Your ad was successfully created.')
        return redirect(url_for('platform.index'))

    return render_template('platform/create_ad.html', title='Create Ad', form=form)


@platform_bp.route('/delete_ad/<ad_id>', methods=['GET', 'POST'])
@login_required
def delete_ad(ad_id):
    Ad.get_by_id(ad_id).delete()
    flash('Ad was deleted.')
    return redirect(url_for('platform.profile', username=current_user.username))


@platform_bp.route('/search_ad', methods=['GET', 'POST'])
def search_ad():
    form = SearchForm()
    form.categories.choices = [(category.name, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        ads = Ad.query

        if form.text_description.data:
            ads = ads.filter(Ad.text_description.contains(form.text_description.data))
        if form.location.data:
            ads = ads.filter(Ad.location.contains(form.location.data))
        if form.price_from.data:
            ads = ads.filter(Ad.price >= form.price_from.data)
        if form.price_to.data:
            ads = ads.filter(Ad.price <= form.price_to.data)

        filtered_ads = []

        if form.categories.data:
            for ad in ads.all():
                categories_match = [category in [c.name for c in ad.categories] for category in form.categories.data]
                if False not in categories_match:
                    filtered_ads.append(ad)

        return render_template(
            'platform/index.html',
            user=current_user,
            ads=sorted(filtered_ads, key=lambda ad: ad.is_paid, reverse=True) if form.categories.data else sorted(ads.all(), key=lambda ad: ad.is_paid, reverse=True)
        )

    return render_template('platform/search_ad.html', title='Search', form=form)


@platform_bp.route('/make_payment/<ad_id>', methods=['GET', 'POST'])
@login_required
def make_payment(ad_id):
    form = PaymentForm()

    if form.validate_on_submit():
        Ad.get_by_id(ad_id).update(is_paid=True)
        flash('Ad is paid now.')
        return redirect(url_for('platform.profile', username=current_user.username))

    return render_template('platform/make_payment.html', title='Make Payment', form=form)


@platform_bp.route('/cancel_payment/<ad_id>', methods=['GET', 'POST'])
@login_required
def cancel_payment(ad_id):
    Ad.get_by_id(ad_id).update(is_paid=False)
    flash('Ad\'s payment was cancelled.')
    return redirect(url_for('platform.profile', username=current_user.username))
