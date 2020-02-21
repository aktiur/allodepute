<script>
  import { depute, random } from "./stores";
  import { deputeAuHasard } from "./back";
  import PhotoDepute from "./PhotoDepute.svelte";

  const click = async () => {
    depute.set(await deputeAuHasard());
  };
</script>

<style>
  .au-hasard {
    display: block;
    margin: 0 0 4rem auto;
  }
</style>

<h4>
  {$depute.article_indefini} {$depute.titre}
  {$random ? 'au hasard' : 'au choix'}
</h4>

<div>
  <h5>{$depute.nom}</h5>
  <p>
    {$depute.titre} {$depute.groupe} de la
    {@html $depute.circonscription}
  </p>
</div>
<PhotoDepute depute={$depute} i={1} extraClasses="adroite" />

<a class="au-hasard" href="#" on:click|preventDefault={click}>
  Donnez-moi un autre député au hasard
</a>
