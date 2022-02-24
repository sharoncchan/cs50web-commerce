from django.contrib import admin

from.models import User, Category, Listing, Bid, Comment, Watchlist

# Register your models here.

admin.site.register(User)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display =['name','slug']
    prepopulated_fields = {'slug':('name',)}


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}


admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)