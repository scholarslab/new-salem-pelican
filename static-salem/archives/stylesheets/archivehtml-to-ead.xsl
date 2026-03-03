<?xml version="1.0" encoding="UTF-8"?>
<!-- this works with MassHist, BPL with some minor manual editing -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
	<xsl:template match="/">
		<ead>
			<archdesc level="collection">
				<dsc type="combined">
					<c01 level="series">
						<did>
							<unittitle>title</unittitle>
						</did>
						<xsl:apply-templates select="descendant::tr"/>
					</c01>
				</dsc>
			</archdesc>
		</ead>
	</xsl:template>

	<xsl:template match="tr">
		<c02 level="item">
			<did>
				<unitid>
					<xsl:value-of select="td[3]"/>
				</unitid>
				<unittitle>
					<xsl:if test="string(normalize-space(td[1]))">
						<persname>
							<xsl:value-of select="td[1]"/>
						</persname>
					</xsl:if>
					<xsl:text> </xsl:text>
					<xsl:value-of select="td[2]"/>
				</unittitle>
				<daogrp>
					<xsl:for-each select="td[3]/a">
						<daoloc id="{substring-before(@href, '.html')}r"/>
						<daoloc id="{substring-before(@href, '.html')}v"/>
					</xsl:for-each>
				</daogrp>
			</did>
			<!--<bibliography>
				<bibref>
					<xsl:text>Page </xsl:text>
					<xsl:value-of select="td[2]"/>
				</bibref>
			</bibliography>-->
		</c02>
	</xsl:template>
</xsl:stylesheet>
