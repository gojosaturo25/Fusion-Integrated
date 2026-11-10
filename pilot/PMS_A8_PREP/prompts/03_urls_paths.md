modules/patent/api/urls.py registers every view with a DRF DefaultRouter, but all of these views are APIView/generic views, not ViewSets, so Django fails with "has no attribute get_extra_actions". Rewrite modules/patent/api/urls.py without any router:
- keep the same two import blocks from .views and .views_legal;
- import only path from django.urls;
- urlpatterns is a plain list of path(...) entries, one per view, each using View.as_view() and the same name as its current basename;
- use the same URL strings, written in Django path syntax: <int:pk> instead of (?P<pk>[0-9]+), and every path ends with a slash;
- give AdminApplicationListView the path "admin/applications/" and ExpireOverdueResubmissionsView the path "admin/expire-resubmissions/" so no two views share a path.
