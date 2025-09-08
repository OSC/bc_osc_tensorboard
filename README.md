# Batch Connect - OSC Tensorboard

![GitHub Release](https://img.shields.io/github/release/osc/bc_osc_tensorboard.svg)
[![GitHub License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

An interactive app designed for OSC OnDemand that launches a TensorBoard
server within an Owens batch job.

## Prerequisites

This Batch Connect app requires the following software be installed on the
**compute nodes** that the batch job is intended to run on (**NOT** the
OnDemand node):

- [Lmod] 6.0.1+ or any other `module purge` and `module load <modules>` based
  CLI used to load appropriate environments within the batch job before
  launching the Tensorboard server.
- [TensorBoard] 2.1.0+ (earlier versions are untested but may work for you)
- [Singularity] 3.5.2+ (earlier versions are untested but may work for you)
- [slirp4netns] 0.4.0+ (earlier versions are untested but may work for you)
- [subuids] need to be enabled for users.

[TensorBoard]: https://www.tensorflow.org/tensorboard
[Lmod]: https://www.tacc.utexas.edu/research-development/tacc-projects/lmod
[Singularity]: https://sylabs.io/singularity/
[slirp4netns]: https://github.com/rootless-containers/slirp4netns
[subuids]: http://man7.org/linux/man-pages/man5/subuid.5.html

## Install

Use Git to clone this app and checkout the desired branch/version you want to
use:

```sh
scl enable git19 -- git clone <repo>
cd <dir>
scl enable git19 -- git checkout <tag/branch>
module load python/3.6-conda5.2
# sudo will install globally, without it pip will install the user's home
sudo python -m pip install -r requirements.txt
```

You will not need to do anything beyond this as all necessary assets are
installed. You will also not need to restart this app as it isn't a Passenger
app.

To update the app you would:

```sh
cd <dir>
scl enable git19 -- git fetch
scl enable git19 -- git checkout <tag/branch>
```

Again, you do not need to restart the app as it isn't a Passenger app.

## Contributing

1. Fork it ( https://github.com/OSC/bc\_osc\_tensorboard/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

## Software used

### authrevproxy
[authrevproxy.py](/template/bin/authrevproxy.py) originally from [stanford-rc/sh\_ood-apps/sh\_tensorboard](https://github.com/stanford-rc/sh_ood-apps/blob/960986941a7ff740a5731e2fc025a95e8e2f7f28/sh_tensorboard/template/bin/authrevproxy.py).

[License](https://github.com/stanford-rc/sh_ood-apps/blob/bff2d7ad21541c0bf68d7412b2e6cdbd282eacda/LICENSE) added in licenses folder.
