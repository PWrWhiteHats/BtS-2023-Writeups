<script>
export default {
  props: ['profile'],
}
</script>

<template>
  <div class="col-12 bg-dark p-3 rounded-3">
    <div class="border-bottom mb-5">
      <h2>About me</h2>
    </div>

    <div class="">

        <!-- location -->
        <div class="row mb-2">
          <div class="col-2 fw-bold">Location</div>
          <div class="col">{{ profile.location }}</div>
        </div>

        <!-- birthday -->
        <div class="row mb-2">
          <div class="col-2 fw-bold">Birthday</div>
          <div class="col">{{ profile.birthday }}</div>
        </div>

    </div>
  </div>
</template>
