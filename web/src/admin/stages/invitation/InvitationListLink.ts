import { DEFAULT_CONFIG } from "@goauthentik/common/api/config";
import { AKElement } from "@goauthentik/elements/Base";

import { t } from "@lingui/macro";

import { CSSResult, TemplateResult, html } from "lit";
import { customElement, property } from "lit/decorators.js";
import { until } from "lit/directives/until.js";

import AKGlobal from "@goauthentik/common/styles/authentik.css";
import PFDescriptionList from "@patternfly/patternfly/components/DescriptionList/description-list.css";
import PFForm from "@patternfly/patternfly/components/Form/form.css";
import PFFormControl from "@patternfly/patternfly/components/FormControl/form-control.css";
import PFFlex from "@patternfly/patternfly/layouts/Flex/flex.css";
import PFBase from "@patternfly/patternfly/patternfly-base.css";

import { StagesApi } from "@goauthentik/api";

@customElement("ak-stage-invitation-list-link")
export class InvitationListLink extends AKElement {
    @property()
    invitation?: string;

    @property()
    selectedFlow?: string;

    static get styles(): CSSResult[] {
        return [PFBase, PFForm, PFFormControl, PFFlex, PFDescriptionList, AKGlobal];
    }

    renderLink(): string {
        return `${window.location.protocol}//${window.location.host}/if/flow/${this.selectedFlow}/?itoken=${this.invitation}`;
    }

    render(): TemplateResult {
        return html`<dl class="pf-c-description-list pf-m-horizontal">
            <div class="pf-c-description-list__group">
                <dt class="pf-c-description-list__term">
                    <span class="pf-c-description-list__text">${t`Select an enrollment flow`}</span>
                </dt>
                <dd class="pf-c-description-list__description">
                    <div class="pf-c-description-list__text">
                        <select
                            class="pf-c-form-control"
                            @change=${(ev: Event) => {
                                const current = (ev.target as HTMLInputElement).value;
                                this.selectedFlow = current;
                            }}
                        >
                            ${until(
                                new StagesApi(DEFAULT_CONFIG)
                                    .stagesInvitationStagesList({
                                        ordering: "name",
                                        noFlows: false,
                                    })
                                    .then((stages) => {
                                        if (
                                            !this.selectedFlow &&
                                            stages.results.length > 0 &&
                                            stages.results[0].flowSet
                                        ) {
                                            this.selectedFlow = stages.results[0].flowSet[0].slug;
                                        }
                                        const seenFlowSlugs: string[] = [];
                                        return stages.results.map((stage) => {
                                            return stage.flowSet?.map((flow) => {
                                                if (seenFlowSlugs.includes(flow.slug)) {
                                                    return html``;
                                                }
                                                seenFlowSlugs.push(flow.slug);
                                                return html`<option
                                                    value=${flow.slug}
                                                    ?selected=${flow.slug === this.selectedFlow}
                                                >
                                                    ${flow.slug}
                                                </option>`;
                                            });
                                        });
                                    }),
                                html`<option>${t`Loading...`}</option>`,
                            )}
                        </select>
                    </div>
                </dd>
            </div>
            <div class="pf-c-description-list__group">
                <dt class="pf-c-description-list__term">
                    <span class="pf-c-description-list__text"
                        >${t`Link to use the invitation.`}</span
                    >
                </dt>
                <dd class="pf-c-description-list__description">
                    <div class="pf-c-description-list__text">
                        <input
                            class="pf-c-form-control"
                            readonly
                            type="text"
                            value=${this.renderLink()}
                        />
                    </div>
                </dd>
            </div>
        </dl>`;
    }
}
