from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Experience, Interest
from main.permissions import (
    IsPortfolioOwnerOrEditorOrReadOnly,
    IsPortfolioOwnerOrReadOnly,
)
from main.serializers import ExperienceSerializer, InterestSerializer


# ============================================================
# EXPERIENCE API VIEWS (TUTORIAL 7)
# ============================================================


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def experience_list(request):
    if request.method == "GET":
        experiences = (
            Experience.objects.prefetch_related("starred_by")
            .order_by("title", "id")
        )
        title = request.query_params.get("title", "").strip()
        if title:
            experiences = experiences.filter(title__icontains=title)
        serializer = ExperienceSerializer(
            experiences, many=True, context={"request": request}
        )
        return Response(serializer.data)

    serializer = ExperienceSerializer(
        data=request.data, context={"request": request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def experience_detail(request, id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"), pk=id
    )

    if request.method == "GET":
        serializer = ExperienceSerializer(
            experience, context={"request": request}
        )
        return Response(serializer.data)

    if request.method in ("PUT", "PATCH"):
        serializer = ExperienceSerializer(
            experience,
            data=request.data,
            partial=(request.method == "PATCH"),
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    experience.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, id):
    experience = get_object_or_404(Experience, pk=id)

    if request.user in experience.starred_by.all():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)

    serializer = ExperienceSerializer(
        experience, context={"request": request}
    )
    return Response(serializer.data)


# ============================================================
# INTEREST API VIEWS (TUGAS 6)
# ============================================================


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def interest_list(request):
    if request.method == "GET":
        interests = (
            Interest.objects.prefetch_related("starred_by")
            .order_by("title", "id")
        )
        title = request.query_params.get("title", "").strip()
        if title:
            interests = interests.filter(title__icontains=title)
        serializer = InterestSerializer(
            interests, many=True, context={"request": request}
        )
        return Response(serializer.data)

    serializer = InterestSerializer(
        data=request.data, context={"request": request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def interest_detail(request, id):
    interest = get_object_or_404(
        Interest.objects.prefetch_related("starred_by"), pk=id
    )

    if request.method == "GET":
        serializer = InterestSerializer(
            interest, context={"request": request}
        )
        return Response(serializer.data)

    if request.method in ("PUT", "PATCH"):
        serializer = InterestSerializer(
            interest,
            data=request.data,
            partial=(request.method == "PATCH"),
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    interest.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def interest_star(request, id):
    interest = get_object_or_404(Interest, pk=id)

    if request.user in interest.starred_by.all():
        interest.starred_by.remove(request.user)
    else:
        interest.starred_by.add(request.user)

    serializer = InterestSerializer(
        interest, context={"request": request}
    )
    return Response(serializer.data)
