%define tarball xf86-video-mga
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

%define gitdate 20080102

Summary:   Xorg X11 mga video driver
Name:      xorg-x11-drv-mga
Version:   1.4.12
Release:   2%{?dist}
URL:       http://www.x.org
License: MIT
Group:     User Interface/X Hardware Support
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:   http://x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
#Source0:    %{tarball}-%{gitdate}.tar.bz2
Source1:    mga.xinf

Patch0: mga-1.4.5-no-hal-advertising.patch
Patch1: mga-1.4.6.1-get-client-pointer.patch
Patch2: mga-1.4.10-g200se-24-not-32.patch

ExcludeArch: s390 s390x

BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-sdk >= 1.4.99.1
BuildRequires: mesa-libGL-devel >= 6.4-4
BuildRequires: libdrm-devel >= 2.0-1

Requires:  hwdata
Requires:  xorg-x11-server-Xorg >= 1.4.99.1

%description 
X.Org X11 mga video driver.

%prep
%setup -q -n %{tarball}-%{version}
%patch0 -p1 -b .hal
%patch1 -p1 -b .gcp
%patch2 -p1 -b .24bpp

%build
autoreconf -v --install || exit 1
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases/

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/mga_drv.so
%{_datadir}/hwdata/videoaliases/mga.xinf
%{_mandir}/man4/mga.4*

%changelog
* Thu Jun 24 2010 Adam Jackson <ajax@redhat.com> 1.4.12-2
- mga-1.4.10-g200se-24-not-32.patch: Prefer 24bpp on G200SE-A (#607093)

* Tue May 18 2010 Adam Jackson <ajax@redhat.com> 1.4.12-1
- mga 1.4.12 (#517924)
- mga.xinf: Update to match.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.4.11-1.1
- Rebuilt for RHEL 6

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 1.4.11-1
- mga 1.4.11

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.10-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 1.4.10-2.1
- ABI bump

* Tue Jun 23 2009 Dave Airlie <airlied@redhat.com> 1.4.10-2
- fixup ABI for rawhide

* Mon Apr 27 2009 Adam Jackson <ajax@redhat.com> 1.4.10-1
- mga 1.4.10

* Tue Feb 24 2009 Adam Jackson <ajax@redhat.com> 1.4.9-2
- Fix ftbfs

* Sun Feb 08 2009 Adam Jackson <ajax@redhat.com> 1.4.9-1
- mga 1.4.9

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 1.4.8-2
- bump for server API change

* Fri Feb 22 2008 Adam Jackson <ajax@redhat.com> 1.4.8-1
- mga 1.4.8

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.7-2.20080102
- Autorebuild for GCC 4.3

* Wed Jan 09 2008 Adam Jackson <ajax@redhat.com> 1.4.7-1.20080102
- Rebuild for new server ABI.

* Wed Jan 02 2008 Adam Jackson <ajax@redhat.com> 1.4.7-0.20080102
- Today's git snapshot for pciaccess goodness.
- mga-1.4.7-death-to-cfb.patch: Remove what little cfb support there was.
- mga-1.4.7-alloca.patch: Fix ALLOCATE_LOCAL references.

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.4.6.1-6
- Rebuild for PPC toolchain bug

* Wed Jun 27 2007 Adam Jackson <ajax@redhat.com> 1.4.6.1-5
- Use %%{?_smp_mflags}.

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.4.6.1-4
- Update Requires and BuildRequires.  Add Requires: hwdata.

* Mon Feb 26 2007 Adam Jackson <ajax@redhat.com> 1.4.6.1-3
- Late-bind a call into a loadable module
- Disown the module directory

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 1.4.6.1-2
- ExclusiveArch -> ExcludeArch
- DRI on all arches

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 1.4.6.1-1
- Update to 1.4.6.1

* Mon Dec 4 2006 Adam Jackson <ajax@redhat.com> 1.4.5-2
- mga-1.4.5-no-hal-advertising.patch: Don't link to the HAL module as it's
  non-free.

* Fri Dec 1 2006 Adam Jackson <ajax@redhat.com> 1.4.5-1
- Update to 1.4.5.

* Fri Aug 18 2006 Kristian Høgsberg <krh@redhat.com> 1.4.1-5.fc6
- Add Tilman Sauerbecks patch to fix DRI locking.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.4.1-4.1
- rebuild

* Thu Jul  6 2006 Adam Jackson <ajackson@redhat.com> 1.4.1-4
- mga.xinf updates.  Add G200SE cards, remove Impression and Mistral IDs
  (since they do not and never have worked), and comment each line with
  the appropriate card name.

* Fri May 26 2006 Mike A. Harris <mharris@redhat.com> 1.4.1-3
- Added with_dri conditionalization (not yet working for non-dri case).
- Added "BuildRequires: libdrm-devel >= 2.0-1" for (#192358).
- Added "BuildRequires: mesa-libGL-devel >= 6.4-4".
- Bumped sdk dep to pick up proto-devel indirectly.

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 1.4.1-2
- Update to 1.4.1 from 7.1RC1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.2.1.3-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.2.1.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.2.1.3-1
- Updated xorg-x11-drv-mga to version 1.2.1.3 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.2.1.2-1
- Updated xorg-x11-drv-mga to version 1.2.1.2 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.2.1-1
- Updated xorg-x11-drv-mga to version 1.2.1 from X11R7 RC2

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 1.2.0.1-1
- Updated xorg-x11-drv-mga to version 1.2.0.1 from X11R7 RC1
- Fix *.la file removal.
- Remove hardware specific {_bindir}/stormdwg utility.

* Mon Oct 3 2005 Mike A. Harris <mharris@redhat.com> 1.1.2-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Limit "ExclusiveArch" to x86, x86_64, ia64, ppc

* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 1.1.2-0
- Initial spec file for mga video driver generated automatically
  by my xorg-driverspecgen script.
