"""Generate sigconf-highlighted.tex: the clean sigconf.tex plus pale-yellow revision markup.

sigconf.tex stays the clean publication source. This script copies it and wraps the
passages that changed relative to the original submission
(../Phosiological-legibolity/iss2026_poster_extended_abstract.tex) in markup macros:

  \\rev{...}      line-breakable highlight for running text (soul's \\hl)
  \\revbox{...}   unbreakable highlight for headings and short labels
  \\revcite{...}  highlighted citation (soul cannot highlight inside \\cite)
  \\revcs         control space usable inside \\rev (soul rejects a literal "\\ ")

Every span is an exact string replacement; a span that no longer matches aborts
the run. check_highlighted.py verifies that removing the markup gives back
sigconf.tex unchanged.

Usage (from the repository root): python revision/make_highlighted.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "sigconf.tex")
OUT = os.path.join(ROOT, "sigconf-highlighted.tex")

PREAMBLE_ANCHOR = "\\definecolor{iconcue}{HTML}{248C87}\n"
MARKUP = r"""
%% ---- BEGIN REVISION MARKUP (review copy only; sigconf.tex is the clean source) ----
%% Highlights changes relative to the original ISS 2026 poster submission.
\usepackage{soul}
\definecolor{revhl}{HTML}{FFF3A3}
\sethlcolor{revhl}
\DeclareRobustCommand{\rev}[1]{\hl{#1}}
\DeclareRobustCommand{\revbox}[1]{{\setlength{\fboxsep}{0pt}\colorbox{revhl}{\strut #1}}}
\DeclareRobustCommand{\revcite}[1]{\revbox{\cite{#1}}}
\newcommand{\revcs}{\ }
\soulregister{\revbox}{7}
\soulregister{\revcite}{7}
\soulregister{\ref}{7}
\soulregister{\revcs}{0}
%% ---- END REVISION MARKUP ----
"""


def rev(text):
    """Wrap running text in \\rev{}, converting citations and control spaces to soul-safe forms."""
    return "\\rev{" + text.replace("\\cite{", "\\revcite{").replace("vs.\\ ", "vs.\\revcs ") + "}"


def heading(cmd, title):
    return f"\\{cmd}{{{title}}}", f"\\{cmd}{{\\texorpdfstring{{\\revbox{{{title}}}}}{{{title}}}}}"


# (exact text in sigconf.tex, replacement) -- in document order.
SPANS = [
    # Abstract: comparison wording; mission-score claim removed.
    ("showed no statistically significant difference from Numeric Cue in teammate awareness, with lower workload and perceived invasiveness.",
     None),
    ("scored higher on coordination usefulness and trust. Together", "@scored higher on coordination usefulness and trust.@ Together"),
    # Teaser caption.
    ("Each remote teammate has a physiological halo; HR sets its pulse and glow, and HRV the coherence of its ring. The physiological cue carries no numeric readout or emotion label.",
     None),
    # Contribution (3).
    ("shows no statistically significant difference from Numeric Cue on teammate awareness,", None),
    ("remains higher on coordination usefulness and trust.", None),
    # Study 1: recognition framing, analysis, qualitative method.
    ("This is a recognition task: viewers judged isolated halo stimuli whose intended states were known.", None),
    ("\\textbf{Analysis.}", None),
    ("participant-level accuracy was compared with chance using two-sided one-sample $t$ tests, with Cohen's $d_z$. All four pre-specified legibility comparisons also survived a conservative Bonferroni threshold of $\\alpha=.0125$. Planned linear trends were Holm-corrected across five tests. Free-text interpretations and open responses were analyzed using reflexive thematic analysis \\cite{braun_using_2006}.",
     None),
    ("\\textbf{Results.} Participants", "@\\textbf{Results.}@ Participants"),
    # Study 2 method: scripted events vs live input.
    ("Each mission included three researcher-triggered task events: \\emph{Ingredient Bottleneck} near 2:00, when two orders required the same ingredient; \\emph{Pot Overload} near 4:30, when two pots became active close together; and \\emph{Service Rush} in the final phase, when completed dishes, dirty plates, and delivery tasks accumulated. These events targeted Prep, Cook, and Runner, respectively. Physiological input remained live; the task events were scripted.",
     None),
    # Figure 5: new apparatus panel.
    ("\\caption{Apparatus}", "\\caption{\\rev{Apparatus}}"),
    ("the participant apparatus with Apple Watch,", None),
    # Measures and Analysis (new subsection).
    heading("subsection", "Measures and Analysis"),
    ("\\textbf{Support response time} was measured in seconds from actual pressure-event onset to the first relevant support action by another teammate. \\textbf{Appropriate support actions} were coded separately: a support action was appropriate when it matched the immediate task need, for example passing ingredients, covering a pot, plating a dish, or delivering an order. Appropriateness was contextual rather than an intrinsic property of an action, so response time marks when support began, whereas the appropriate-support count captures whether support fit the need. Event logs recorded action type, appropriateness, prior verbal requests, and cue references. Service Rush also assessed whether appropriate support occurred within ten seconds. \\textbf{Recovery time} was measured in seconds from actual pressure-event onset until the task bottleneck was resolved: the required ingredients had been prepared and supplied for both affected orders (Ingredient Bottleneck), both affected pots had been cleared (Pot Overload), or the dishes, dirty plates, and deliveries pending at event onset had been processed (Service Rush). Successful dish retrieval and burning were distinguished; newly arriving work was excluded from the Service Rush endpoint. Unresolved events were recorded as unrecovered. This measure describes task recovery, not physiological recovery.",
     None),
    ("Behavioral outcomes were analyzed at the team-by-condition level ($n=12$ teams), using repeated-measures ANOVA and planned two-sided paired $t$ contrasts (Icon versus No Cue, Icon versus Numeric, and Numeric versus No Cue), with Cohen's $d_z$. The primary contrast was Icon versus No Cue for support response time. The 108 pressure events were nested within 12 teams, not treated as independent observations. Questionnaire comparisons used participant-by-condition paired $t$ tests ($n=36$ participants) over the same three contrasts. Analyses used Python with pandas, SciPy, and statsmodels.",
     None),
    ("Team communication was coded post hoc into eight categories: task instructions, support offers, status checks, uncertainty statements, help requests, strategy changes, physiological references, and numeric references. Coding relied on one primary coder without a verified reliability sample. Category frequencies were compared at the team-by-condition level with Friedman tests followed by Wilcoxon signed-rank pairwise contrasts. Answers to the closing open-ended questions were coded with theme labels applied during data collection; this is distinct from Study~1's reflexive thematic analysis.",
     None),
    heading("subsection", "Results"),
    # Results: display fidelity vs comprehension; added statistics and definitions.
    ("from the cue-present conditions. This agreement establishes display fidelity, not observer comprehension (Section~\\ref{sec:scope}).", None),
    ("($t(11)=-4.49$, $p=.001$, $d_z=-1.30$)", None),
    ("($t(11)=-1.81$, $p=.098$, $d_z=-0.52$)", None),
    ("Task recovery time decreased from 29.0\\,s under No Cue to 23.2\\,s under Icon Cue ($t(11)=-5.31$, $p<.001$, $d_z=-1.53$). Teams logged more appropriate support actions under Numeric Cue (3.17) and Icon Cue (3.42) than under No Cue (2.25; descriptive team means, Figure~\\ref{fig:s2results}d).",
     None),
    ("(Friedman tests, all $p<.001$; corresponding Wilcoxon contrasts, all $p\\leq.002$)", None),
    # Figure 6: mission-score panel removed; caption rewritten.
    ("\\caption{Team performance: orders delivered, error count, and appropriate support actions.}",
     "\\caption{\\rev{Team performance: orders delivered, error count, and appropriate support actions.}}"),
    ("(a) support response and task recovery by pressure event; (b) post-condition ratings; (c) final preferences; and (d) orders delivered, errors, and appropriate support actions. In (d), gray lines show team-level means and black markers show condition means $\\pm$ 95\\% CI.",
     None),
    # Awareness / workload / ratings.
    ("with no statistically significant difference from Numeric Cue", None),
    ("The four-item workload mean had low internal consistency (Cronbach's $\\alpha=.13$) and should be interpreted descriptively rather than as a validated composite.", None),
    ("Numeric Cue was rated higher on coordination usefulness (5.50 vs.\\ 5.30, $p=.023$) and trust (5.55 vs.\\ 5.24, $p=.002$)", None),
    # Discussion.
    heading("section", "Discussion and Limitations"),
    ("No statistically significant difference in teammate awareness was detected between Icon and Numeric Cue. Icon Cue had lower reported workload and perceived invasiveness, but Numeric Cue scored higher on coordination usefulness and trust.",
     None),
    ("\\textbf{What the scripted events do and do not show.}\\label{sec:scope} ",
     "\\rev{\\textbf{What the scripted events do and do not show.}}\\label{sec:scope} "),
    ("The two studies support different claims. Study~1 tested \\emph{recognition}: whether viewers could identify the intended HR and HRV state of isolated halos. In Study~2, \\emph{physiological input was live}, but the \\emph{task-pressure events were scripted}; event onset is the behavioral timing reference and does not establish a particular physiological response in the overloaded player. Agreement between \\emph{displayed and classified states} shows that the halo rendered what the classifier produced. It does not show that teammates \\emph{understood the intended cue information} during a given event: Study~2 included no event-specific comprehension check. Faster assistance under a cue may therefore also reflect visible task difficulty in the shared game view or verbal communication, not the physiological information alone.",
     None),
    ("\\textbf{Collaborative XR spaces.} Avatar placement in social AR is sensitive to the available physical space and meeting context \\cite{drago_exploring_2025}, while digital-proxemics research examines how display and audio affordances relate to personal space, proximity, and attention in virtual collaboration \\cite{williamson_digital_2022}. These findings motivate studying avatar-associated physiological halos in collaborative AR/VR rather than assuming that a fixed desktop HUD transfers unchanged: where a halo is placed relative to an avatar or seat, how proximity and attention change its visibility, and who in a shared space may see it. A future evaluation could compare HUD-based and spatially anchored cues during joint tasks, measuring cue interpretation, support response, workload, and perceived invasiveness while examining proximity, occlusion, and audience-specific sharing permissions. This is a proposed extension: the current desktop-game studies do not establish effectiveness in XR.",
     None),
    ("The reported results do not establish that teammates correctly interpreted the physiological cue during individual scripted pressure events. Communication was coded by a single primary coder without a verified reliability sample.",
     None),
    # Conclusion.
    ("showed no statistically significant difference from Numeric Cue in teammate awareness, with lower workload and perceived invasiveness, while Numeric Cue yielded higher coordination usefulness and trust.",
     None),
    # Ethics / Data / AI Use: own subsection; AI disclosure made consistent.
    heading("subsection", "Ethics / Data / AI Use"),
    ("Generative AI tools (ChatGPT and Claude Code) were used for language editing and restructuring of author-drafted text. During this revision, ChatGPT also assisted with identifying related literature, and Claude Code assisted with LaTeX formatting and checking reference metadata. These tools were not used to generate participant data or reported statistical results. The authors verified all sources, reviewed the final text, and take responsibility for it.",
     None),
]


def main():
    s = open(SRC, encoding="utf-8").read()
    assert s.count(PREAMBLE_ANCHOR) == 1
    s = s.replace(PREAMBLE_ANCHOR, PREAMBLE_ANCHOR + MARKUP, 1)
    for old, new in SPANS:
        if new is None:
            new = rev(old)
        elif "@" in new:  # @...@ marks the part of the replacement to highlight
            pre, mid, post = new.split("@")
            new = pre + rev(mid) + post
        n = s.count(old)
        if n != 1:
            raise SystemExit(f"span matched {n} times (expected 1): {old[:70]}...")
        s = s.replace(old, new, 1)
    s = s.replace(
        "%% ACM ISS 2026 Poster track -- camera-ready extended abstract (two-column sigconf).",
        "%% ACM ISS 2026 Poster track -- REVIEW COPY with highlighted revisions (generated by\n"
        "%% revision/make_highlighted.py from sigconf.tex; do not edit by hand, do not submit to TAPS).", 1)
    open(OUT, "w", encoding="utf-8", newline="\n").write(s)
    print(f"wrote {OUT} with {len(SPANS)} highlighted spans")


if __name__ == "__main__":
    main()
