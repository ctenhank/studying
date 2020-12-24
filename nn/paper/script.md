# Script

-----------------

we could conclude that the facts of all photos mainly comes from two aspects.

The real unstructured distortion such as blurry color fading some slight blur and structured distortion such as scratches and dust.

our target here is to solve them together with the only one network. 

---

---

we first introduce some previous work on mixed degradation restoration. 

basically they want to restore one corrupted image from its synthetic degraded version the noise blur and JPEG compression of different levels will be injected into one natural images to construct the paired data.

Then the training will be processed by the synthetic pairs.

There are mainly two drawbacks.

firstly their trained models may not generalize to real old photos well.

secondly they only focused on the local degradation and don't handle the global defects such as restoring the broken region.

------

---

ideally we can't train the network on synthetic dataset.

however the real degradation can be rather complicated and there is always a gap between the synthetic data and real photos. 

so the learned network may not generalize well on real ones to solve the domain gap.

we propose a triplet domain translation framework.

the idea is that we project the two image domains into a latent space.

this latet space assumes an Gaussian prior and has a compact structure so it is easier to close the gap in this space.

then we learn the decoder which maps the latent subspace to clean images.

 the decoder can be learned using the synthetic training pairs.

because the gap has been reduced the same decoder can also work well for real photos.

---

---

this slids shows the network's structure basically there's two VAEs.

the first VAE encodes old photos and synthetic images into a shared latent space and second VAE obtains the latent code of clean images.

since synthetic image and clean images are paired data now we can learn the mapping between their latent spaces.

this means no matter what kind of degradation exists int input image.

we want to obtain one clean and complete image finally.

we also design modules for this latent mapping network so that it can achieve multiple tasks such as the denoising, color correction image inpainting and so on.

and the residual blocks of domain translation network mainly focus on the local defects.

It cannot capture a long-term dependency relationship

we design another partial non-local block to assist the inpainting tasks

specifically given one intermediate feature map of transition Network 

-------------------------------

and the corresponding down-sampled mask. 

we calculate the normalized similarity between the hole region pixels and non-hole region pixels through the embedded Gaussian function. 

Based on the global context feature we could generate the new feature map combing original local features and new generated features.

we fuse them together according to the mask.

our method is compared with previous works.

-------------------

the table shows that on synthetic dataset

our method is always among the top in terms of various metrics

 the advantage on real photos is more obvious

our method gives much more compelling results

here are more results we also tested on portraits

of celebrities after restoration

these photos could look like the

photograph is taken by modern

cameras and you could find more

details in this website and feel free to contact

me if there are any questions

that's al